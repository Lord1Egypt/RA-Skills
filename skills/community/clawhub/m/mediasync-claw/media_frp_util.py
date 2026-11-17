import os
import sys
import platform
import stat
import subprocess
import hashlib
import time
import requests
import zipfile
import tarfile
import io
from uuid_config import UUIDConfig

FRP_VERSION = "0.65.0"

# ── Per-platform SHA256 checksums for frp v0.65.0 ──
# Source: https://github.com/fatedier/frp/releases/tag/v0.65.0
# Run the following to obtain checksums for a new version:
#   curl -sL https://github.com/fatedier/frp/releases/download/v<VERSION>/frp_<VERSION>_checksums.txt
FRP_CHECKSUMS = {
    "windows_amd64": {
        "archive": "5885bff09604e719e429698f800f89379f3910f07490ca1f7d8a7f7a40970eda",
        "binary":  "5b0846d4a5e9bcde0960b354fd819eb0011529ff23f41ad55a8717ba5c7004ac",
    },
    "darwin_amd64": {
        "archive": "83dcf7617c61bef0087cb771e99fd16d749203c16dd6bbf47efb15ce617dc471",
        "binary":  "1cdbf2589fd2924d2d387d5350c6a4b4f5cecae2c6dbc594691e78dcc5fa52c7",
    },
    "darwin_arm64": {
        "archive": "bce3badaf40cf5d3811c9eae593f3b24833bf7cb13b8b7c3f9453e94af45ded1",
        "binary":  "c52b7f0d66b49a9da5d00de864aa3dfcdfd6ff214c9b5f8d72d019d1a4ae48d2",
    }
}

uuid_config_instance = UUIDConfig()


def get_domain():
    uuid_value = uuid_config_instance.get_uuid()
    return uuid_value + ".yunfrp.net"


def detect_platform():
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "windows":
        if machine in ("amd64", "x86_64"):
            return "windows_amd64"
    elif system == "darwin":
        if machine in ("arm64", "aarch64"):
            return "darwin_arm64"
        elif machine in ("amd64", "x86_64"):
            return "darwin_amd64"

    raise RuntimeError(f"Unsupported platform: {system} / {machine}")


def get_frpc_binary_name():
    if sys.platform == "win32":
        return "frpc.exe"
    else:
        return "frpc"


def get_frp_archive_name(plat):
    ext = "zip" if plat.startswith("windows") else "tar.gz"
    return f"frp_{FRP_VERSION}_{plat}.{ext}"


def get_frpc_name_in_archive(plat):
    if plat.startswith("windows"):
        return "frpc.exe"
    else:
        return "frpc"


def download_frp():
    plat = detect_platform()
    checksums = FRP_CHECKSUMS.get(plat)
    if checksums is None:
        print(f"[FRP] ERROR: No checksums configured for platform: {plat}")
        return False

    current_directory = os.path.dirname(os.path.abspath(__file__))
    frpc_binary_name = get_frpc_binary_name()
    frpc_path = os.path.join(current_directory, frpc_binary_name)

    if os.path.exists(frpc_path):
        return True

    archive_name = get_frp_archive_name(plat)
    frp_url = f"https://github.com/fatedier/frp/releases/download/v{FRP_VERSION}/{archive_name}"

    try:
        print(f"[FRP] Downloading {frpc_binary_name} v{FRP_VERSION} for {plat}...")
        r = requests.get(frp_url, timeout=120)
        r.raise_for_status()

        archive_data = r.content

        archive_hash = hashlib.sha256(archive_data).hexdigest()
        if archive_hash != checksums["archive"]:
            print(f"[FRP] SECURITY ERROR: Archive checksum mismatch!")
            print(f"  Expected: {checksums['archive']}")
            print(f"  Got:      {archive_hash}")
            print(f"  The download may have been tampered with or corrupted. Aborting.")
            return False
        print(f"[FRP] Archive SHA256 verified: {archive_hash[:16]}...")

        frpc_name_in_archive = get_frpc_name_in_archive(plat)

        if plat.startswith("windows"):
            with zipfile.ZipFile(io.BytesIO(archive_data)) as zf:
                frpc_member = None
                for member in zf.namelist():
                    if member.endswith(frpc_name_in_archive):
                        frpc_member = member
                        break

                if not frpc_member:
                    print(f"[FRP] ERROR: {frpc_name_in_archive} not found in archive.")
                    return False

                binary_data = zf.read(frpc_member)
        else:
            with tarfile.open(fileobj=io.BytesIO(archive_data), mode="r:gz") as tf:
                frpc_member = None
                for member in tf.getnames():
                    if member.endswith(frpc_name_in_archive):
                        frpc_member = member
                        break

                if not frpc_member:
                    print(f"[FRP] ERROR: {frpc_name_in_archive} not found in archive.")
                    return False

                f = tf.extractfile(frpc_member)
                if f is None:
                    print(f"[FRP] ERROR: Failed to extract {frpc_name_in_archive}.")
                    return False
                binary_data = f.read()

        binary_hash = hashlib.sha256(binary_data).hexdigest()
        if binary_hash != checksums["binary"]:
            print(f"[FRP] SECURITY ERROR: {frpc_name_in_archive} checksum mismatch!")
            print(f"  Expected: {checksums['binary']}")
            print(f"  Got:      {binary_hash}")
            print(f"  Aborting.")
            return False
        print(f"[FRP] {frpc_name_in_archive} SHA256 verified: {binary_hash[:16]}...")

        with open(frpc_path, "wb") as f:
            f.write(binary_data)

        if not plat.startswith("windows"):
            current_perms = os.stat(frpc_path).st_mode
            os.chmod(frpc_path, current_perms | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            print(f"[FRP] Execute permission set on {frpc_binary_name}")

        print(f"[FRP] {frpc_binary_name} v{FRP_VERSION} downloaded and verified successfully.")
        return True

    except requests.RequestException as e:
        print(f"[FRP] Network error downloading frpc: {e}")
        return False
    except Exception as e:
        print(f"[FRP] Unexpected error: {e}")
        return False


def setup_frp_and_keep_alive(port=8000, frp_config=None, stop_event=None):
    print(f"DEBUG: setup_frp called with local_port={port}, frp_config={frp_config}")

    if frp_config is None:
        frp_domain = get_domain()
        frp_config_content = f'''
            serverAddr = "129.213.174.213"
            serverPort = 7000

            webServer.addr = "127.0.0.1"
            webServer.port = 7400

            [transport]
            heartbeatInterval = 30
            heartbeatTimeout = 90
            tcpMux = true
            tcpMuxKeepaliveInterval = 30

            [[proxies]]
            name = "{frp_domain}"
            type = "http"
            customDomains = ["{frp_domain}"]
            localPort = {port}
        '''
        frp_config = "frpc.toml"
        with open(frp_config, 'w') as f:
            f.write(frp_config_content.strip())

        print(f"Started FRP tunnel using config: {frp_config_content}")

    current_directory = os.path.dirname(os.path.abspath(__file__))
    resolved_config = os.path.realpath(os.path.join(current_directory, frp_config))
    if not resolved_config.startswith(os.path.realpath(current_directory) + os.sep):
        raise ValueError(f"FRP config path outside allowed directory: {frp_config}")

    frp_process = None
    frpc_binary_name = get_frpc_binary_name()
    try:
        frpc_path = os.path.join(current_directory, frpc_binary_name)
        if not os.path.isfile(frpc_path):
            raise FileNotFoundError(f"FRP client not found: {frpc_path}")
        if not os.path.isfile(resolved_config):
            raise FileNotFoundError(f"FRP config not found: {resolved_config}")

        frp_process = subprocess.Popen(
            [frpc_path, '-c', resolved_config],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False)
        while not (stop_event and stop_event.is_set()):
            poll_result = frp_process.poll()

            if poll_result is not None:
                if stop_event and stop_event.is_set():
                    break
                frp_process = subprocess.Popen(
                    [frpc_path, '-c', resolved_config],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=False)
                continue

            time.sleep(1)
    except Exception as e:
        print(f"Error: FRP client failed to start: {frpc_path}. Error: {e}")
        print(f"Please ensure {frpc_binary_name} is in the media-file-server directory")
    finally:
        if frp_process and frp_process.poll() is None:
            frp_process.terminate()
            try:
                frp_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                frp_process.kill()
            print("[FRP] frpc stopped.")


def setup_frp(port=8000, stop_event=None):
    if not download_frp():
        print("Error: Failed to download frpc")
        return

    import threading
    frp_thread = threading.Thread(target=setup_frp_and_keep_alive, args=(port, None, stop_event), daemon=True)
    frp_thread.start()