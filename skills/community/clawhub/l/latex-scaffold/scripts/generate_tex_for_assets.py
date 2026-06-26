import os
from pathlib import Path
import argparse

TEX_FIG = r"""\begin{figure*}[htb]
    \centering
    \includegraphics[width=0.5\linewidth]{SOURCE}
    \caption{TODO}
    \label{fig:NAME}
\end{figure*}"""


def generate_tex(src: Path):
    dst = src.with_suffix(".tex")
    if dst.exists(): return
    code = TEX_FIG.replace("SOURCE", src.as_posix()).replace("NAME", str(src.stem))
    dst.write_text(code)
    print(f"Generated: {dst}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path, help="Root directory of the LaTeX project")
    args = parser.parse_args()

    # assets
    os.chdir(args.root)
    ASSETS = Path("assets")
    assert ASSETS.exists(), f"`{ASSETS.resolve()}` does not exist"

    # figure
    for pat in ("*.png", "*.jpg"):
        for src in ASSETS.rglob(pat):
            generate_tex(src)
