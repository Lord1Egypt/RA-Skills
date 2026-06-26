#!/usr/bin/env python3
"""Extract mermaid blocks from markdown, render to PNG, replace with image refs."""
import sys, re, subprocess, os

infile, outfile, imgdir = sys.argv[1], sys.argv[2], sys.argv[3]
content = open(infile).read()
idx = 0

def replace_mermaid(m):
    global idx
    mmd = os.path.join(imgdir, f"mermaid_{idx}.mmd")
    png = os.path.join(imgdir, f"mermaid_{idx}.png")
    with open(mmd, 'w') as f:
        f.write(m.group(1))
    subprocess.run(
        ["mmdc", "-i", mmd, "-o", png, "-b", "transparent", "--width", "1200"],
        stdin=subprocess.DEVNULL, capture_output=True, timeout=30
    )
    idx += 1
    if os.path.exists(png):
        return f"![mermaid]({png})"
    return m.group(0)

content = re.sub(r'```mermaid\n(.*?)```', replace_mermaid, content, flags=re.DOTALL)
open(outfile, 'w').write(content)
