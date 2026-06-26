import subprocess, os

JAR_PATH = os.path.join(os.path.dirname(__file__), "plantuml.jar")

def render(tmp_file, fmt="png", output_path=None):
    """Render PlantUML source to an image.

    Returns the base64‑encoded image data.
    """
    if not os.path.exists(JAR_PATH):
        raise FileNotFoundError(f"PlantUML JAR not found at {JAR_PATH}")
    # with tempfile.NamedTemporaryFile(suffix=".puml", delete=False, mode="w") as tmp:
    #     tmp.write(source)
    #     tmp_file = tmp.name
    out_dir = os.path.dirname(output_path) if output_path else None
    cmd = ["java", "-jar", JAR_PATH, f"-t{fmt}"]
    if out_dir:
        cmd += ["-o", out_dir]
    cmd.append(tmp_file)
    subprocess.run(cmd, check=True)
    img_path = output_path or os.path.join(os.path.dirname(tmp_file), os.path.splitext(os.path.basename(tmp_file))[0]+f".{fmt}")
    print(f"image path {img_path}")

# Entry point for skill invocation
if __name__ == "__main__":
    import sys
    render(sys.argv[1])
