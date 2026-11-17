import argparse
import asyncio
import base64
import math
import os
import sys
import time
from array import array

from openai import AsyncOpenAI
from openai.types.live.session_config_param import SessionConfigParam


MODEL = "gpt-live-1"
VOICE = os.environ.get("SPEAK_LIVE_VOICE", "cedar")

SAMPLE_RATE = 24000
BYTES_PER_SAMPLE = 2

START_BUFFER_MS = int(
    os.environ.get("SPEAK_BUFFER_MS", "200")
)

MAX_PREBUFFER_WAIT_SECONDS = 1.5
START_TIMEOUT_SECONDS = 15.0

# Fine frase: nessuna voce significativa e nessun nuovo
# transcript per questo intervallo.
END_QUIET_SECONDS = float(
    os.environ.get("SPEAK_END_QUIET", "1.8")
)

# Soglia RMS per distinguere voce reale da chunk quasi silenziosi.
VOICE_RMS_THRESHOLD = int(
    os.environ.get("SPEAK_RMS_THRESHOLD", "120")
)

LIVE_KEEPALIVE_MS = 100

ALSA_DEVICE = os.environ.get(
    "SPEAK_ALSA_DEVICE",
    "default",
)

DEBUG = os.environ.get("SPEAK_DEBUG") == "1"


START_BUFFER_BYTES = (
    SAMPLE_RATE
    * BYTES_PER_SAMPLE
    * START_BUFFER_MS
    // 1000
)

LIVE_SILENCE_BYTES = (
    b"\x00\x00"
    * (SAMPLE_RATE * LIVE_KEEPALIVE_MS // 1000)
)

LIVE_SILENCE_B64 = base64.b64encode(
    LIVE_SILENCE_BYTES
).decode("ascii")


def pcm_rms(data: bytes) -> float:
    usable = len(data) - (len(data) % 2)

    if usable <= 0:
        return 0.0

    samples = array("h")
    samples.frombytes(data[:usable])

    if sys.byteorder != "little":
        samples.byteswap()

    if not samples:
        return 0.0

    mean_square = sum(
        sample * sample
        for sample in samples
    ) / len(samples)

    return math.sqrt(mean_square)


async def wait_for_session_started(connection):
    while True:
        event = await asyncio.wait_for(
            connection.recv(),
            timeout=10.0,
        )

        if DEBUG:
            print("EVENT:", event.type)

        if event.type == "session.started":
            return

        if event.type == "error":
            raise RuntimeError(
                f"GPT-Live error [{event.error.code}]: "
                f"{event.error.message}"
            )


async def create_player():
    stderr = (
        None
        if DEBUG
        else asyncio.subprocess.DEVNULL
    )

    return await asyncio.create_subprocess_exec(
        "aplay",
        "-q",
        "-D",
        ALSA_DEVICE,
        "-t",
        "raw",
        "-f",
        "S16_LE",
        "-r",
        str(SAMPLE_RATE),
        "-c",
        "1",
        stdin=asyncio.subprocess.PIPE,
        stderr=stderr,
    )


async def keep_live_input_alive(
    connection,
    stop_event,
):
    while not stop_event.is_set():
        await connection.session.input_audio.append(
            audio=LIVE_SILENCE_B64
        )

        try:
            await asyncio.wait_for(
                stop_event.wait(),
                timeout=LIVE_KEEPALIVE_MS / 1000,
            )
        except asyncio.TimeoutError:
            pass


async def receive_live_audio(
    connection,
    audio_queue,
):
    received_audio = False
    heard_voice = False

    started_at = time.monotonic()
    last_meaningful_activity = None

    transcript_parts = []

    try:
        while True:
            now = time.monotonic()

            if (
                not received_audio
                and now - started_at >= START_TIMEOUT_SECONDS
            ):
                raise RuntimeError(
                    "GPT-Live did not produce audio"
                )

            if (
                heard_voice
                and last_meaningful_activity is not None
                and now - last_meaningful_activity
                >= END_QUIET_SECONDS
            ):
                if DEBUG:
                    print(
                        "Utterance complete after "
                        f"{END_QUIET_SECONDS:.1f}s "
                        "without meaningful activity."
                    )

                break

            try:
                event = await asyncio.wait_for(
                    connection.recv(),
                    timeout=0.1,
                )

            except asyncio.TimeoutError:
                continue

            if DEBUG:
                print("EVENT:", event.type)

            if event.type == "session.output_audio.delta":
                audio = base64.b64decode(event.delta)

                received_audio = True

                level = pcm_rms(audio)

                if DEBUG:
                    print(f"RMS: {level:.0f}")

                if level >= VOICE_RMS_THRESHOLD:
                    heard_voice = True
                    last_meaningful_activity = time.monotonic()

                # Riproduciamo comunque tutti i chunk ricevuti,
                # inclusi i silenzi naturali tra le parole.
                await audio_queue.put(audio)

            elif event.type == "session.output_transcript.delta":
                transcript_parts.append(event.delta)

                if event.delta.strip():
                    heard_voice = True
                    last_meaningful_activity = time.monotonic()

            elif event.type == "error":
                raise RuntimeError(
                    f"GPT-Live error [{event.error.code}]: "
                    f"{event.error.message}"
                )

    finally:
        await audio_queue.put(None)

        if DEBUG and transcript_parts:
            print(
                "TRANSCRIPT:",
                "".join(transcript_parts),
            )


async def play_buffered_audio(audio_queue):
    initial_chunks = []
    initial_bytes = 0
    first_audio_at = None
    stream_finished = False

    #
    # PREBUFFER
    #
    while True:
        if first_audio_at is None:
            item = await audio_queue.get()

        else:
            elapsed = (
                time.monotonic()
                - first_audio_at
            )

            remaining = (
                MAX_PREBUFFER_WAIT_SECONDS
                - elapsed
            )

            if remaining <= 0:
                break

            try:
                item = await asyncio.wait_for(
                    audio_queue.get(),
                    timeout=min(
                        0.1,
                        remaining,
                    ),
                )

            except asyncio.TimeoutError:
                continue

        if item is None:
            stream_finished = True
            break

        if first_audio_at is None:
            first_audio_at = time.monotonic()

        initial_chunks.append(item)
        initial_bytes += len(item)

        if initial_bytes >= START_BUFFER_BYTES:
            break

    if not initial_chunks:
        return

    if DEBUG:
        buffered_ms = (
            initial_bytes
            / (
                SAMPLE_RATE
                * BYTES_PER_SAMPLE
            )
            * 1000
        )

        print(
            f"Starting playback with "
            f"{buffered_ms:.0f} ms buffered"
        )

    #
    # PLAYBACK CONTINUO
    #
    player = await create_player()

    if player.stdin is None:
        raise RuntimeError(
            "Audio player stdin unavailable"
        )

    try:
        for chunk in initial_chunks:
            player.stdin.write(chunk)

        await player.stdin.drain()

        if not stream_finished:
            while True:
                chunk = await audio_queue.get()

                if chunk is None:
                    break

                player.stdin.write(chunk)
                await player.stdin.drain()

    finally:
        player.stdin.close()
        await player.wait()


async def speak(text):
    text = text.strip()

    if not text:
        raise ValueError(
            "Text cannot be empty"
        )

    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is not set"
        )

    session: SessionConfigParam = {
        "model": MODEL,

        "instructions": (
            "You are the voice renderer for an "
            "embodied AI agent. "
            "Speak Italian naturally, warmly and concisely. "
            "Use an adult, calm, warm, slightly low-pitched "
            "speaking style. "
            "When commentary is supplied, communicate it "
            "aloud immediately and naturally. "
            "Do not add introductions or unrelated information."
        ),

        "audio": {
            "format": {
                "type": "audio/pcm",
                "rate": SAMPLE_RATE,
            },

            "output": {
                "voice": VOICE,
            },
        },

        "delegation": {
            "type": "client",
        },

        "store": False,
    }

    audio_queue = asyncio.Queue()
    stop_keepalive = asyncio.Event()

    async with AsyncOpenAI() as client:
        async with client.live.connect() as connection:
            await connection.session.start(
                session=session,
                event_id="ruben_speak_start",
            )

            await wait_for_session_started(
                connection
            )

            await connection.session.input_audio.append(
                audio=LIVE_SILENCE_B64
            )

            receiver_task = asyncio.create_task(
                receive_live_audio(
                    connection,
                    audio_queue,
                )
            )

            keepalive_task = asyncio.create_task(
                keep_live_input_alive(
                    connection,
                    stop_keepalive,
                )
            )

            player_task = asyncio.create_task(
                play_buffered_audio(
                    audio_queue,
                )
            )

            await connection.session.commentary.append(
                content=text,
                delegation_id=None,
                event_id="ruben_speak_commentary",
            )

            try:
                await asyncio.gather(
                    receiver_task,
                    player_task,
                )

            finally:
                stop_keepalive.set()

                try:
                    await keepalive_task
                except asyncio.CancelledError:
                    pass

                for task in (
                    receiver_task,
                    player_task,
                ):
                    if not task.done():
                        task.cancel()

                await asyncio.gather(
                    receiver_task,
                    player_task,
                    return_exceptions=True,
                )

            await connection.session.close(
                event_id="ruben_speak_close"
            )


def main():
    parser = argparse.ArgumentParser(
        description="Speak through Ruben's GPT-Live voice."
    )

    parser.add_argument(
        "text",
        help="Text Ruben should say",
    )

    args = parser.parse_args()

    asyncio.run(
        speak(args.text)
    )


if __name__ == "__main__":
    main()
