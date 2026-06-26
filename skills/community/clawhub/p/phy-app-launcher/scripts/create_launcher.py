#!/Users/haoyangpang/.claude/skills/app-launcher/venv/bin/python3
"""
Create a macOS .app launcher for local dev projects.
Click the app icon → runs dev server in Terminal.

Features:
- Auto-detect project type and start command
- Auto-generate app icon using FAL AI (--auto-icon)
- Convert PNG to ICNS using PIL for reliability
"""

import os
import sys
import stat
import shutil
import subprocess
from pathlib import Path

# Optional: FAL AI for icon generation
try:
    import fal_client
    FAL_AVAILABLE = True
    # Set FAL API key if not already set
    if not os.environ.get("FAL_KEY"):
        os.environ["FAL_KEY"] = "958bbaef-1ee3-46af-a0fa-3cdc50f6f0a3:960afb2bfe0cbc654e657e581e1955cb"
except ImportError:
    FAL_AVAILABLE = False

# Optional: PIL for reliable PNG handling
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

def generate_icon_with_fal(app_name: str, output_path: str = None) -> str:
    """Generate an app icon using FAL AI.

    Args:
        app_name: Name of the app (used for prompt)
        output_path: Where to save the icon (default: /tmp/{app_name}-icon.png)

    Returns:
        Path to generated icon
    """
    if not FAL_AVAILABLE:
        print("Warning: fal_client not installed. Install with: pip install fal-client")
        return None

    if output_path is None:
        safe_name = app_name.lower().replace(" ", "-").replace("_", "-")
        output_path = f"/tmp/{safe_name}-icon.png"

    # Create a macOS Big Sur style app icon prompt
    prompt = f"""macOS Big Sur app icon for "{app_name}".
Dark gradient background (deep blue to purple), squircle shape filling the frame.
Simple centered glowing symbol representing the app's purpose.
Minimalist, clean, professional software icon.
NO TEXT, NO LETTERS, only abstract iconography.
Apple design language, subtle glass effect, soft glow."""

    try:
        result = fal_client.subscribe(
            "fal-ai/flux/schnell",
            arguments={
                "prompt": prompt,
                "image_size": "square",
                "num_images": 1,
            },
        )

        image_url = result["images"][0]["url"]

        # Download the image
        import urllib.request
        urllib.request.urlretrieve(image_url, output_path)

        print(f"✓ Generated icon: {output_path}")
        return output_path

    except Exception as e:
        print(f"Warning: Could not generate icon: {e}")
        return None


def convert_png_to_icns(png_path: str, icns_path: str) -> bool:
    """Convert PNG to ICNS using PIL for reliable results.

    Args:
        png_path: Path to source PNG
        icns_path: Path to output ICNS

    Returns:
        True if successful
    """
    if not PIL_AVAILABLE:
        print("Warning: PIL not installed. Install with: pip install Pillow")
        return False

    try:
        # Create iconset directory
        iconset_dir = icns_path.replace(".icns", ".iconset")
        os.makedirs(iconset_dir, exist_ok=True)

        # Load source image
        img = Image.open(png_path).convert("RGBA")

        # Required sizes for macOS icons
        sizes = [
            (16, "icon_16x16.png"),
            (32, "icon_16x16@2x.png"),
            (32, "icon_32x32.png"),
            (64, "icon_32x32@2x.png"),
            (128, "icon_128x128.png"),
            (256, "icon_128x128@2x.png"),
            (256, "icon_256x256.png"),
            (512, "icon_256x256@2x.png"),
            (512, "icon_512x512.png"),
            (1024, "icon_512x512@2x.png"),
        ]

        for size, name in sizes:
            resized = img.resize((size, size), Image.LANCZOS)
            output_file = os.path.join(iconset_dir, name)
            resized.save(output_file, "PNG")

        # Convert iconset to icns using iconutil
        result = subprocess.run(
            ["iconutil", "-c", "icns", iconset_dir, "-o", icns_path],
            capture_output=True,
            text=True
        )

        # Cleanup iconset
        shutil.rmtree(iconset_dir)

        if result.returncode == 0:
            print(f"✓ Created ICNS: {icns_path}")
            return True
        else:
            print(f"Warning: iconutil failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"Warning: Could not convert to ICNS: {e}")
        return False


def detect_project_type(project_path: Path) -> dict:
    """Detect project type and return start command."""

    # Check for package.json (Node.js)
    package_json = project_path / "package.json"
    if package_json.exists():
        import json
        with open(package_json) as f:
            pkg = json.load(f)
        scripts = pkg.get("scripts", {})

        # Priority: dev > start > serve
        if "dev" in scripts:
            return {"type": "node", "cmd": "npm run dev", "name": pkg.get("name", project_path.name)}
        elif "start" in scripts:
            return {"type": "node", "cmd": "npm start", "name": pkg.get("name", project_path.name)}
        elif "serve" in scripts:
            return {"type": "node", "cmd": "npm run serve", "name": pkg.get("name", project_path.name)}

    # Check for Python projects
    if (project_path / "pyproject.toml").exists() or (project_path / "setup.py").exists():
        # Check for common entry points
        if (project_path / "app.py").exists():
            return {"type": "python", "cmd": "python app.py", "name": project_path.name}
        elif (project_path / "main.py").exists():
            return {"type": "python", "cmd": "python main.py", "name": project_path.name}
        elif (project_path / "manage.py").exists():  # Django
            return {"type": "python", "cmd": "python manage.py runserver", "name": project_path.name}

    # Check for specific files
    if (project_path / "app.py").exists():
        return {"type": "python", "cmd": "python app.py", "name": project_path.name}
    if (project_path / "main.py").exists():
        return {"type": "python", "cmd": "python main.py", "name": project_path.name}

    # Check for Makefile
    if (project_path / "Makefile").exists():
        return {"type": "make", "cmd": "make dev", "name": project_path.name}

    # Check for docker-compose
    if (project_path / "docker-compose.yml").exists() or (project_path / "docker-compose.yaml").exists():
        return {"type": "docker", "cmd": "docker-compose up", "name": project_path.name}

    return {"type": "unknown", "cmd": None, "name": project_path.name}


def create_app_bundle(
    project_path: str,
    app_name: str = None,
    start_cmd: str = None,
    icon_path: str = None,
    output_dir: str = None,
    auto_icon: bool = False
) -> str:
    """
    Create a macOS .app bundle that launches the dev server.

    Args:
        project_path: Path to the project directory
        app_name: Name for the .app (default: project folder name)
        start_cmd: Command to run (default: auto-detect)
        icon_path: Path to .icns or .png icon (optional)
        output_dir: Where to save the .app (default: ~/Desktop)
        auto_icon: If True, auto-generate icon using FAL AI when no icon provided

    Returns:
        Path to the created .app bundle
    """
    project_path = Path(project_path).resolve()

    if not project_path.exists():
        raise ValueError(f"Project path does not exist: {project_path}")

    # Auto-detect project info
    project_info = detect_project_type(project_path)

    if app_name is None:
        app_name = project_info["name"]

    if start_cmd is None:
        start_cmd = project_info["cmd"]
        if start_cmd is None:
            raise ValueError(f"Could not detect start command. Please specify with --cmd")

    if output_dir is None:
        output_dir = Path.home() / "Desktop"
    else:
        output_dir = Path(output_dir)

    # Create .app bundle structure
    app_bundle = output_dir / f"{app_name}.app"
    contents_dir = app_bundle / "Contents"
    macos_dir = contents_dir / "MacOS"
    resources_dir = contents_dir / "Resources"

    # Remove existing bundle if present
    if app_bundle.exists():
        shutil.rmtree(app_bundle)

    # Create directories
    macos_dir.mkdir(parents=True)
    resources_dir.mkdir(parents=True)

    # Check for venv
    venv_activate = ""
    if (project_path / "venv").exists():
        venv_activate = "source venv/bin/activate && "
    elif (project_path / ".venv").exists():
        venv_activate = "source .venv/bin/activate && "

    # Create the launcher script
    launcher_script = macos_dir / "launcher"
    script_content = f'''#!/bin/bash
# Auto-generated launcher for {app_name}

cd "{project_path}"

# Open new Terminal window and run the dev server
osascript -e 'tell application "Terminal"
    activate
    do script "cd \\"{project_path}\\" && {venv_activate}{start_cmd}"
end tell'
'''

    launcher_script.write_text(script_content)
    launcher_script.chmod(launcher_script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    # Create Info.plist
    info_plist = contents_dir / "Info.plist"
    bundle_id = app_name.lower().replace(" ", "-").replace("_", "-")

    plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>launcher</string>
    <key>CFBundleIdentifier</key>
    <string>com.devlauncher.{bundle_id}</string>
    <key>CFBundleName</key>
    <string>{app_name}</string>
    <key>CFBundleDisplayName</key>
    <string>{app_name}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>LSUIElement</key>
    <false/>
</dict>
</plist>
'''
    info_plist.write_text(plist_content)

    # Handle icon
    # Auto-generate if requested and no icon provided
    if auto_icon and not icon_path:
        icon_path = generate_icon_with_fal(app_name)

    icon_applied = False
    if icon_path:
        icon_path = Path(icon_path)
        if icon_path.exists():
            icns_dest = resources_dir / "AppIcon.icns"

            if icon_path.suffix == ".icns":
                shutil.copy(icon_path, icns_dest)
                icon_applied = True
            elif icon_path.suffix in [".png", ".jpg", ".jpeg"]:
                # Convert to icns using PIL (more reliable than sips)
                if convert_png_to_icns(str(icon_path), str(icns_dest)):
                    icon_applied = True
                else:
                    # Fallback: try sips if PIL not available
                    try:
                        iconset_path = resources_dir / "AppIcon.iconset"
                        iconset_path.mkdir()

                        sizes = [16, 32, 64, 128, 256, 512]
                        for size in sizes:
                            subprocess.run([
                                "sips", "-z", str(size), str(size),
                                str(icon_path), "--out", str(iconset_path / f"icon_{size}x{size}.png")
                            ], capture_output=True)
                            if size <= 256:
                                subprocess.run([
                                    "sips", "-z", str(size*2), str(size*2),
                                    str(icon_path), "--out", str(iconset_path / f"icon_{size}x{size}@2x.png")
                                ], capture_output=True)

                        subprocess.run([
                            "iconutil", "-c", "icns", str(iconset_path), "-o", str(icns_dest)
                        ], capture_output=True)
                        shutil.rmtree(iconset_path)

                        if icns_dest.exists():
                            icon_applied = True
                    except Exception as e:
                        print(f"Warning: Could not convert icon: {e}")

    # Update plist with icon if applied
    if icon_applied:
        plist_content = plist_content.replace(
            "</dict>\n</plist>",
            "    <key>CFBundleIconFile</key>\n    <string>AppIcon</string>\n</dict>\n</plist>"
        )
        info_plist.write_text(plist_content)

    print(f"✓ Created: {app_bundle}")
    print(f"  Project: {project_path}")
    print(f"  Command: {start_cmd}")
    if icon_applied:
        print(f"  Icon: {icon_path} → AppIcon.icns")

    return str(app_bundle)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Create a macOS .app launcher for dev projects"
    )
    parser.add_argument("project_path", help="Path to the project directory")
    parser.add_argument("--name", help="App name (default: project folder name)")
    parser.add_argument("--cmd", help="Start command (default: auto-detect)")
    parser.add_argument("--icon", help="Path to icon file (.icns or .png)")
    parser.add_argument("--output", help="Output directory (default: ~/Desktop)")
    parser.add_argument("--auto-icon", action="store_true",
                        help="Auto-generate icon using FAL AI (requires fal_client)")

    args = parser.parse_args()

    try:
        create_app_bundle(
            project_path=args.project_path,
            app_name=args.name,
            start_cmd=args.cmd,
            icon_path=args.icon,
            output_dir=args.output,
            auto_icon=args.auto_icon
        )
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
