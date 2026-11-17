# paste-safe-pi — Worked Examples

Concrete before/after for the two failure modes. All commands are pure ASCII,
short, single-line, and followed by a read-back.

## Example 1: Bad multi-line heredoc -> good sed

BAD (breaks on paste — every body line gets a 2-space indent, and the user
cannot copy the block at all):

```
cat > tune_grasp.py <<'EOF'
def place_and_home(ch5_place, ch4_grab):
    set_servo(6, PLACE_CH6); _s(2.5)
    set_servo(4, ch4_grab); _s(2.0)
EOF
```

GOOD (one line per change, read-back to confirm):

```
sed -i '63s/ch4_grab); _s(2.0)/ch4_grab-20); _s(2.0)/' tune_grasp.py
sed -n '63p' tune_grasp.py
```

## Example 2: Bad long one-liner -> good split

BAD (110 chars, terminal wraps it and inserts a real newline mid-argument):

```
python3 tune_grasp.py 5 --ch6 92 --ch5 145 --ch4 180 --ch3 75 --ch5p 185 --ch6p 38
```

GOOD (split into two short lines; the second reuses stored params):

```
sed -i "/5: dict/s/ch5=140/ch5=145/" main_pipeline_vision.py
python3 tune_grasp.py 5 --ch4p 160
```

## Example 3: Pattern with a slash -> alternate delimiter

The line contains `/`, so `/` as the sed delimiter fights quoting. Switch to `|`:

```
sed -i '30s|/home/pi/x|/home/pi/medarm|' start.sh
sed -n '30p' start.sh
```

## Example 4: Garbled non-ASCII in a replacement

BAD (Chinese label typed into the command — arrives as mojibake on the Pi,
corrupting the file):

```
sed -i '64s/松爪/松開/' tune_grasp.py
```

GOOD (don't touch the Chinese text; address by position and replace only an
ASCII fragment, or leave the label alone and only change the ASCII argument):

```
sed -i '64s/CH_OPEN/120/' tune_grasp.py
sed -n '64p' tune_grasp.py
```

## Example 5: Range address (def line through next blank line)

When you don't know the exact line number, address a range from a pattern to the
next blank line, then narrow the replacement to an ASCII fragment:

```
sed -i '/^def place_and_home/,/^$/s/PLACE_CH6/ch6_place/' tune_grasp.py
sed -n '/place_and_home/,/^$/p' tune_grasp.py
```

## Example 6: Append a single line (no heredoc)

```
echo 'PLACE_CH6 = 38' >> config.py
tail -1 config.py
```

## Anti-pattern quick reference

| Anti-pattern              | Why it breaks on paste        | Use instead            |
|---------------------------|-------------------------------|------------------------|
| heredoc `<<'EOF'` block   | 2-space indent on body lines  | `sed -i` per change    |
| 100+ char one-liner       | wraps, stray newline mid-arg  | split into 2 commands  |
| Chinese in `sed` pattern | mojibake corrupts pattern     | ASCII fragment pattern |
| `VAR=x; cmd $VAR`         | user must also copy VAR line  | bake value into cmd    |
| `for i in ...; do ...; done` | continuation indent breaks | one `sed` per change   |
