from __future__ import annotations

import argparse
import importlib
from dataclasses import dataclass
from io import BytesIO
import json
import shutil
import subprocess
import sys
from pathlib import Path


def _run_install(package_name: str) -> None:
    ensure_commands = [
        [sys.executable, "-m", "ensurepip", "--upgrade"],
    ]
    install_commands = [
        [sys.executable, "-m", "pip", "install", package_name],
    ]
    uv_path = shutil.which("uv")
    if uv_path:
        install_commands.append([uv_path, "pip", "install", "--python", sys.executable, package_name])

    for ensure_command in ensure_commands:
        subprocess.run(ensure_command, check=False)

    last_error: Exception | None = None
    for command in install_commands:
        try:
            subprocess.run(command, check=True)
            return
        except Exception as exc:  # noqa: BLE001
            last_error = exc
    if last_error is not None:
        raise last_error


def _candidate_browsers() -> list[tuple[str, str]]:
    candidates: list[tuple[str, str]] = []

    command_names = [
        ("chrome", "google-chrome"),
        ("chrome", "google-chrome-stable"),
        ("chromium", "chromium"),
        ("chromium", "chromium-browser"),
        ("edge", "microsoft-edge"),
        ("edge", "msedge"),
        ("brave", "brave-browser"),
        ("brave", "brave"),
    ]
    for label, command in command_names:
        resolved = shutil.which(command)
        if resolved:
            candidates.append((label, resolved))

    home = Path.home()
    platform_specific = [
        ("chrome", Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")),
        ("chrome", Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")),
        ("edge", Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")),
        ("edge", Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe")),
        ("brave", Path(r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe")),
        ("chrome", Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")),
        ("chromium", Path("/Applications/Chromium.app/Contents/MacOS/Chromium")),
        ("edge", Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge")),
        ("brave", Path("/Applications/Brave Browser.app/Contents/MacOS/Brave Browser")),
        ("chrome", home / ".local/bin/google-chrome"),
        ("chromium", Path("/usr/bin/chromium")),
        ("chromium", Path("/usr/bin/chromium-browser")),
        ("edge", Path("/usr/bin/microsoft-edge")),
        ("brave", Path("/usr/bin/brave-browser")),
        ("chromium", Path("/snap/bin/chromium")),
    ]
    for label, candidate in platform_specific:
        if candidate.exists():
            candidates.append((label, str(candidate)))

    deduped: list[tuple[str, str]] = []
    seen: set[str] = set()
    for label, resolved in candidates:
        if resolved not in seen:
            deduped.append((label, resolved))
            seen.add(resolved)
    return deduped


def ensure_playwright_module() -> None:
    try:
        importlib.import_module("playwright.sync_api")
        return
    except ImportError:
        pass

    _run_install("playwright")
    importlib.import_module("playwright.sync_api")


def install_playwright_browser() -> None:
    subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        check=True,
    )


def ensure_pillow() -> None:
    try:
        importlib.import_module("PIL.Image")
        return
    except ImportError:
        pass

    _run_install("pillow")
    importlib.import_module("PIL.Image")


@dataclass(frozen=True)
class CaptureSegment:
    scroll_y: int
    crop_top: int
    crop_bottom: int


def build_capture_segments(
    page_height: int,
    viewport_height: int,
    overlap: int = 200,
) -> list[CaptureSegment]:
    if page_height <= 0:
        raise ValueError("page_height must be positive")
    if viewport_height <= 0:
        raise ValueError("viewport_height must be positive")
    if overlap < 0 or overlap >= viewport_height:
        raise ValueError("overlap must be between 0 and viewport_height - 1")

    if page_height <= viewport_height:
        return [CaptureSegment(scroll_y=0, crop_top=0, crop_bottom=page_height)]

    step = viewport_height - overlap
    max_scroll = page_height - viewport_height
    positions = [0]

    while positions[-1] < max_scroll:
        next_scroll = min(positions[-1] + step, max_scroll)
        if next_scroll == positions[-1]:
            break
        positions.append(next_scroll)

    segments: list[CaptureSegment] = []
    previous_scroll = 0
    for index, scroll_y in enumerate(positions):
        visible_height = min(viewport_height, page_height - scroll_y)
        crop_top = 0 if index == 0 else max(0, previous_scroll + viewport_height - scroll_y)
        crop_bottom = visible_height
        if crop_bottom > crop_top:
            segments.append(
                CaptureSegment(
                    scroll_y=scroll_y,
                    crop_top=crop_top,
                    crop_bottom=crop_bottom,
                )
            )
        previous_scroll = scroll_y

    return segments


def stitch_capture_segments(
    capture_bytes: list[bytes],
    segments: list[CaptureSegment],
    output_image: Path,
    image_format: str,
) -> None:
    ensure_pillow()
    from PIL import Image

    if len(capture_bytes) != len(segments):
        raise ValueError("capture_bytes and segments must have the same length")

    cropped_images: list[Image.Image] = []
    total_height = 0
    output_width = 0

    try:
        for image_bytes, segment in zip(capture_bytes, segments, strict=True):
            with Image.open(BytesIO(image_bytes)) as image:
                cropped = image.crop((0, segment.crop_top, image.width, segment.crop_bottom))
                loaded = cropped.copy()
            cropped_images.append(loaded)
            output_width = max(output_width, loaded.width)
            total_height += loaded.height

        if not cropped_images:
            raise ValueError("at least one screenshot segment is required")

        first_mode = cropped_images[0].mode
        output_mode = "RGB" if image_format == "jpg" else first_mode
        background = (255, 255, 255) if output_mode == "RGB" else (255, 255, 255, 0)
        stitched = Image.new(output_mode, (output_width, total_height), background)
        try:
            cursor_y = 0
            for image in cropped_images:
                prepared = image.convert(output_mode) if image.mode != output_mode else image
                try:
                    stitched.paste(prepared, (0, cursor_y))
                finally:
                    if prepared is not image:
                        prepared.close()
                cursor_y += image.height

            save_kwargs = {"format": image_format.upper()}
            if image_format == "jpg":
                save_kwargs["quality"] = 92
            output_image.parent.mkdir(parents=True, exist_ok=True)
            stitched.save(output_image, **save_kwargs)
        finally:
            stitched.close()
    finally:
        for image in cropped_images:
            image.close()


def _wait_for_page_assets(page) -> None:
    page.evaluate(
        """
        async () => {
            await document.fonts.ready;
            const images = Array.from(document.images);
            await Promise.all(
                images.map((img) => {
                    if (img.complete) return Promise.resolve();
                    return new Promise((resolve) => {
                        img.addEventListener('load', resolve, { once: true });
                        img.addEventListener('error', resolve, { once: true });
                    });
                })
            );
        }
        """
    )


def _capture_page_segments(page, output_image: Path, image_format: str) -> None:
    viewport = page.viewport_size or {"width": 1000, "height": 1400}
    viewport_height = int(viewport["height"])
    page_height = int(
        page.evaluate(
            """
            () => Math.ceil(
                Math.max(
                    document.documentElement.scrollHeight,
                    document.body.scrollHeight,
                )
            )
            """
        )
    )
    overlap = min(200, max(80, viewport_height // 7))
    segments = build_capture_segments(
        page_height=page_height,
        viewport_height=viewport_height,
        overlap=overlap,
    )

    capture_bytes: list[bytes] = []
    for segment in segments:
        page.evaluate(
            """
            async (scrollY) => {
                window.scrollTo(0, scrollY);
                await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
            }
            """,
            segment.scroll_y,
        )
        capture_bytes.append(
            page.screenshot(
                type=image_format,
                full_page=False,
                quality=92 if image_format == "jpg" else None,
                animations="disabled",
            )
        )

    stitch_capture_segments(
        capture_bytes=capture_bytes,
        segments=segments,
        output_image=output_image,
        image_format=image_format,
    )


def _load_page(page, page_url: str) -> None:
    page.goto(page_url, wait_until="load")
    page.wait_for_load_state("networkidle")
    _wait_for_page_assets(page)


def export_image(
    html_path: Path,
    output_image: Path,
    image_format: str = "png",
    browser_executable: str | None = None,
) -> dict[str, str]:
    ensure_playwright_module()
    from playwright.sync_api import sync_playwright

    output_image.parent.mkdir(parents=True, exist_ok=True)
    page_url = html_path.resolve().as_uri()
    browser_candidates = _candidate_browsers()
    launch_errors: list[str] = []

    with sync_playwright() as playwright:
        if browser_executable:
            browser_candidates = [("manual", browser_executable)]

        for label, executable in browser_candidates:
            try:
                browser = playwright.chromium.launch(
                    executable_path=executable,
                    headless=True,
                )
                try:
                    page = browser.new_page(viewport={"width": 1000, "height": 1400})
                    _load_page(page, page_url)
                    _capture_page_segments(page, output_image, image_format)
                    return {
                        "mode": "local-browser",
                        "browser_label": label,
                        "browser_executable": executable,
                        "output_image": str(output_image.resolve()),
                    }
                finally:
                    browser.close()
            except Exception as exc:  # noqa: BLE001
                launch_errors.append(f"{label}:{executable}:{exc}")

        install_playwright_browser()
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page(viewport={"width": 1000, "height": 1400})
            _load_page(page, page_url)
            _capture_page_segments(page, output_image, image_format)
            return {
                "mode": "playwright-installed",
                "browser_label": "playwright-chromium",
                "browser_executable": "",
                "output_image": str(output_image.resolve()),
                "previous_launch_errors": json.dumps(launch_errors, ensure_ascii=False),
            }
        finally:
            browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export a rendered HTML document into a long image."
    )
    parser.add_argument("input_html", help="Path to the rendered HTML file.")
    parser.add_argument("output_image", help="Path to the output PNG/JPG file.")
    parser.add_argument(
        "--format",
        choices=["png", "jpg"],
        default="png",
        help="Image format. Defaults to png.",
    )
    parser.add_argument(
        "--browser-executable",
        default="",
        help="Optional explicit browser executable path.",
    )
    args = parser.parse_args()

    result = export_image(
        html_path=Path(args.input_html).resolve(),
        output_image=Path(args.output_image).resolve(),
        image_format=args.format,
        browser_executable=args.browser_executable or None,
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
