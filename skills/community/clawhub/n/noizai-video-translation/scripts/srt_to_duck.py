#!/usr/bin/env python3
import sys
import re

def main():
    if len(sys.argv) != 3:
        print("Usage: srt_to_duck.py <srt_file> <output_cmd_file>", file=sys.stderr)
        sys.exit(1)
        
    srt_file = sys.argv[1]
    cmd_file = sys.argv[2]
    
    try:
        with open(srt_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading SRT: {e}", file=sys.stderr)
        sys.exit(1)
        
    pattern = r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})"
    matches = re.findall(pattern, content)
    
    commands = []
    # Start with volume 1.0
    commands.append("0.0 [enter] volume volume 1.0;")
    
    for m in matches:
        h1, m1, s1, ms1 = int(m[0]), int(m[1]), int(m[2]), int(m[3])
        h2, m2, s2, ms2 = int(m[4]), int(m[5]), int(m[6]), int(m[7])
        
        start = h1*3600 + m1*60 + s1 + ms1/1000.0
        end = h2*3600 + m2*60 + s2 + ms2/1000.0
        
        # small padding to avoid overlapping commands if timings are tight, 
        # but exact float should be fine.
        commands.append(f"{start:.3f} [enter] volume volume 0.0;")
        commands.append(f"{end:.3f} [enter] volume volume 1.0;")
        
    with open(cmd_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(commands) + "\n")

if __name__ == "__main__":
    main()
