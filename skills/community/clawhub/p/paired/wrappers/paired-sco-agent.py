#!/usr/bin/env python3
"""paired-sco-agent v3 — fd lifecycle aware streaming. CVSD-only."""
import os, sys, json, time, wave, select, argparse, signal, logging, threading
from pathlib import Path
import dbus, dbus.service, dbus.mainloop.glib
from gi.repository import GLib

OFONO_BUS = "org.ofono"
HFP_AUDIO_MGR_IFACE = "org.ofono.HandsfreeAudioManager"
HFP_AUDIO_AGENT_IFACE = "org.ofono.HandsfreeAudioAgent"
VCM_IFACE = "org.ofono.VoiceCallManager"

AGENT_PATH = "/org/${USER}/bt_sco_agent"
MODEM_PATH = "/hfp/org/bluez/hci0/dev_AA_BB_CC_DD_EE_FF"

CODEC_CVSD = 0x01
CODEC_MSBC = 0x02
CVSD_RATE = 8000
CVSD_PKT_SAMPLES = 24
CVSD_PKT_BYTES = 48

STATE_FILE = Path(f"/run/user/{os.getuid()}/paired-sco-agent.json")
DEFAULT_TIMEOUT = 60
ACTIVE_WAIT_TIMEOUT = 45

logging.basicConfig(level=logging.INFO, format="%(asctime)s [paired-sco-agent] %(levelname)s: %(message)s")
log = logging.getLogger()


class HandsfreeAudioAgent(dbus.service.Object):
    def __init__(self, bus, path):
        super().__init__(bus, path)
        self.active_fd = None
        self.active_card = None
        self.active_codec = None
        self.fd_change_event = threading.Event()
        self.released_event = threading.Event()
        self._lock = threading.Lock()

    @dbus.service.method(HFP_AUDIO_AGENT_IFACE, in_signature="ohy", out_signature="")
    def NewConnection(self, card, fd, codec):
        try:
            real_fd = fd.take() if hasattr(fd, "take") else int(fd)
        except Exception:
            real_fd = int(fd)
        codec_int = int(codec)
        with self._lock:
            if self.active_fd is not None:
                log.info(f"NewConnection: closing previous fd={self.active_fd}")
                try: os.close(self.active_fd)
                except OSError: pass
            log.info(f"NewConnection: card={card} fd={real_fd} codec={codec_int}")
            self.active_fd = real_fd
            self.active_card = str(card)
            self.active_codec = codec_int
            self._write_state()
            self.fd_change_event.set()

    @dbus.service.method(HFP_AUDIO_AGENT_IFACE, in_signature="", out_signature="")
    def Release(self):
        log.info("Release called by ofono")
        self._cleanup_fd()
        self._clear_state()
        self.released_event.set()

    def _cleanup_fd(self):
        with self._lock:
            if self.active_fd is not None:
                try: os.close(self.active_fd)
                except OSError: pass
            self.active_fd = None
            self.active_card = None
            self.active_codec = None

    def _write_state(self):
        codec_name = {CODEC_CVSD: "cvsd", CODEC_MSBC: "msbc"}.get(self.active_codec, "unknown")
        rate = 8000 if self.active_codec == CODEC_CVSD else 16000
        data = {"fd": self.active_fd, "card": self.active_card, "codec": self.active_codec,
                "codec_name": codec_name, "sample_rate": rate, "channels": 1,
                "format": "s16le", "agent_pid": os.getpid(), "timestamp": time.time()}
        try:
            STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
            STATE_FILE.write_text(json.dumps(data, indent=2))
        except OSError as e:
            log.error(f"Failed writing state: {e}")

    def _clear_state(self):
        try: STATE_FILE.unlink(missing_ok=True)
        except OSError: pass


def register_agent(bus, agent_path, codecs):
    mgr = dbus.Interface(bus.get_object(OFONO_BUS, "/"), HFP_AUDIO_MGR_IFACE)
    codec_bytes = dbus.Array([dbus.Byte(c) for c in codecs], signature="y")
    mgr.Register(agent_path, codec_bytes)
    log.info(f"Registered HandsfreeAudioAgent at {agent_path} with codecs={list(codecs)}")


def unregister_agent(bus, agent_path):
    try:
        mgr = dbus.Interface(bus.get_object(OFONO_BUS, "/"), HFP_AUDIO_MGR_IFACE)
        mgr.Unregister(agent_path)
    except dbus.DBusException as e:
        if "NotFound" not in str(e):
            log.warning(f"Unregister: {e}")


def get_call_state(bus, modem_path=MODEM_PATH):
    try:
        vcm = dbus.Interface(bus.get_object(OFONO_BUS, modem_path), VCM_IFACE)
        calls = vcm.GetCalls()
        if not calls: return None
        return str(calls[0][1].get("State", "?"))
    except dbus.DBusException:
        return None


def wait_for_active_call(bus, timeout=ACTIVE_WAIT_TIMEOUT, modem_path=MODEM_PATH):
    log.info(f"Waiting up to {timeout}s for call state=active...")
    end = time.time() + timeout
    last_state = None
    while time.time() < end:
        state = get_call_state(bus, modem_path)
        if state != last_state:
            log.info(f"  Call state: {state}")
            last_state = state
        if state == "active":
            log.info("Call is active")
            return True
        if state is None and last_state == "active":
            log.info("Call ended")
            return False
        time.sleep(0.2)
    log.error("Timeout waiting for active state")
    return False


def wait_for_writable(fd, timeout=5.0):
    end = time.time() + timeout
    while time.time() < end:
        try:
            r, w, e = select.select([], [fd], [], 0.1)
            if fd in w: return True
        except (OSError, ValueError):
            return False
    return False


def open_wav_for_read(path, expected_rate=CVSD_RATE):
    w = wave.open(path, "rb")
    if w.getnchannels() != 1:
        w.close(); raise ValueError(f"WAV must be mono, got {w.getnchannels()} channels")
    if w.getsampwidth() != 2:
        w.close(); raise ValueError(f"WAV must be 16-bit, got {w.getsampwidth()*8}-bit")
    if w.getframerate() != expected_rate:
        w.close(); raise ValueError(f"WAV rate {w.getframerate()} != required {expected_rate}")
    return w


def stream_play_into_active(agent, bus, wav_path):
    if not wait_for_active_call(bus):
        return False
    log.info("Waiting briefly for any post-active NewConnection update...")
    time.sleep(1.0)
    fd = agent.active_fd
    if fd is None:
        log.error("No SCO fd captured")
        return False
    if not wait_for_writable(fd, timeout=5.0):
        log.error(f"fd={fd} not writable after waiting")
        return False
    log.info(f"fd={fd} writable, beginning stream")
    w = open_wav_for_read(wav_path, CVSD_RATE)
    pkt = CVSD_PKT_BYTES
    total = 0
    written_packets = 0
    failed_packets = 0
    log.info(f"Playing {wav_path} into SCO fd={fd}...")
    try:
        while True:
            frames = w.readframes(CVSD_PKT_SAMPLES)
            if not frames: break
            if len(frames) < pkt:
                frames = frames + b"\x00" * (pkt - len(frames))
            try:
                n = os.write(fd, frames)
                total += n
                written_packets += 1
            except BlockingIOError:
                if not wait_for_writable(fd, timeout=0.5):
                    log.warning("fd became un-writable mid-stream")
                    break
                continue
            except OSError as e:
                failed_packets += 1
                if failed_packets > 5:
                    log.error(f"SCO write failing repeatedly: errno={e.errno} {e.strerror}")
                    break
        log.info(f"Wrote {total} bytes ({written_packets} packets, {failed_packets} failures)")
        return total > 0
    finally:
        w.close()


def stream_record_from_active(agent, bus, wav_path, duration_sec):
    if not wait_for_active_call(bus):
        return False
    time.sleep(1.0)
    fd = agent.active_fd
    if fd is None: return False
    pkt = CVSD_PKT_BYTES
    end = time.time() + duration_sec
    out = wave.open(wav_path, "wb")
    out.setnchannels(1); out.setsampwidth(2); out.setframerate(CVSD_RATE)
    total = 0; failures = 0
    log.info(f"Recording {duration_sec}s from SCO fd={fd} -> {wav_path}")
    try:
        while time.time() < end:
            try:
                r, _, _ = select.select([fd], [], [], 0.1)
                if fd not in r: continue
                data = os.read(fd, pkt)
                if not data: continue
                out.writeframes(data)
                total += len(data)
            except OSError as e:
                failures += 1
                if failures > 5:
                    log.error(f"SCO read failing: errno={e.errno} {e.strerror}")
                    break
        log.info(f"Read {total} bytes ({total // pkt} packets, {failures} failures)")
        return total > 0
    finally:
        out.close()


def cmd_status():
    if not STATE_FILE.exists():
        print("No active SCO connection (state file missing).")
        return 0
    try:
        print(json.dumps(json.loads(STATE_FILE.read_text()), indent=2))
    except Exception as e:
        print(f"State file unreadable: {e}", file=sys.stderr); return 1
    return 0


def cmd_unregister():
    bus = dbus.SystemBus()
    unregister_agent(bus, AGENT_PATH)
    return 0


def run_with_agent(action_fn, codecs=(CODEC_CVSD,), wait_timeout=DEFAULT_TIMEOUT):
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    agent = HandsfreeAudioAgent(bus, AGENT_PATH)
    try:
        register_agent(bus, AGENT_PATH, codecs)
    except dbus.DBusException as e:
        msg = str(e)
        if "AlreadyExists" in msg or "in use" in msg.lower():
            log.error("Another agent is already registered. Try: paired-sco-agent --unregister")
        else:
            log.error(f"Register failed: {msg}")
        return 2

    loop = GLib.MainLoop()
    threading.Thread(target=loop.run, daemon=True).start()
    rc = 1
    try:
        log.info(f"Waiting up to {wait_timeout}s for first SCO NewConnection...")
        log.info("(Place a call now: ~/bin/bt-call <number>)")
        if not agent.fd_change_event.wait(timeout=wait_timeout):
            log.error("Timeout waiting for SCO connection")
            return 3
        try:
            ok = action_fn(agent, bus)
            rc = 0 if ok else 5
        except Exception as e:
            log.exception(f"Action failed: {e}")
            rc = 4
    finally:
        agent._cleanup_fd()
        agent._clear_state()
        unregister_agent(bus, AGENT_PATH)
        loop.quit()
    return rc


def cmd_daemon():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    agent = HandsfreeAudioAgent(bus, AGENT_PATH)
    try:
        register_agent(bus, AGENT_PATH, [CODEC_CVSD])
    except dbus.DBusException as e:
        log.error(f"Register failed: {e}")
        return 2
    loop = GLib.MainLoop()
    def shutdown(signum, frame):
        log.info(f"Caught signal {signum}, shutting down")
        unregister_agent(bus, AGENT_PATH)
        agent._cleanup_fd()
        agent._clear_state()
        loop.quit()
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    log.info(f"Daemon ready (pid={os.getpid()}). Waiting for SCO connections...")
    try: loop.run()
    finally: unregister_agent(bus, AGENT_PATH)
    return 0


def cmd_once():
    return run_with_agent(lambda agent, bus: (log.info("Captured fd, --once mode complete") or True))


def cmd_play(wav_path):
    if not Path(wav_path).is_file():
        log.error(f"WAV file not found: {wav_path}"); return 1
    return run_with_agent(lambda agent, bus: stream_play_into_active(agent, bus, wav_path))


def cmd_record(seconds, wav_path):
    return run_with_agent(lambda agent, bus: stream_record_from_active(agent, bus, wav_path, seconds))


def cmd_duplex(in_path, out_path, seconds):
    if not Path(in_path).is_file():
        log.error(f"WAV file not found: {in_path}"); return 1
    def action(agent, bus):
        if not wait_for_active_call(bus): return False
        time.sleep(1.0)
        fd = agent.active_fd
        if fd is None: return False
        play_t = threading.Thread(target=stream_play_into_active, args=(agent, bus, in_path))
        rec_t = threading.Thread(target=stream_record_from_active, args=(agent, bus, out_path, seconds))
        rec_t.start(); play_t.start()
        play_t.join(); rec_t.join()
        return True
    return run_with_agent(action)


def main():
    p = argparse.ArgumentParser(description="ofono HandsfreeAudioAgent + SCO stream tool")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--daemon", action="store_true")
    g.add_argument("--once", action="store_true")
    g.add_argument("--status", action="store_true")
    g.add_argument("--unregister", action="store_true")
    g.add_argument("--play", metavar="WAV")
    g.add_argument("--record", nargs=2, metavar=("SECONDS", "WAV"))
    g.add_argument("--duplex", nargs=3, metavar=("IN", "OUT", "SECS"))
    args = p.parse_args()
    if args.status: return cmd_status()
    if args.unregister: return cmd_unregister()
    if args.daemon: return cmd_daemon()
    if args.once: return cmd_once()
    if args.play: return cmd_play(args.play)
    if args.record: return cmd_record(int(args.record[0]), args.record[1])
    if args.duplex: return cmd_duplex(args.duplex[0], args.duplex[1], int(args.duplex[2]))


if __name__ == "__main__":
    sys.exit(main())
