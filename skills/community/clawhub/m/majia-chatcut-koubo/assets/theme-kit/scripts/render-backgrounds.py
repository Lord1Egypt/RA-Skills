from pathlib import Path
from cairosvg import svg2png

root = Path(__file__).resolve().parents[1]
source = root / "assets" / "backgrounds"
target = root / "assets" / "backgrounds-png"
target.mkdir(parents=True, exist_ok=True)
for svg in sorted(source.glob("*.svg")):
    svg2png(url=str(svg), write_to=str(target / f"{svg.stem}.png"), output_width=1080, output_height=1920)
    print("rendered", svg.name)
