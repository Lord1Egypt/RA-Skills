#!/bin/bash
# Overlay Quote Image Generator — dùng ảnh cá nhân ngẫu nhiên từ thư mục
# Usage: ./create-overlay-image.sh "Quote text" output.png
# Or with custom config:
#   PICS_DIR="/path/to/images" \
#   AUTHOR_NAME="Your Name" \
#   AUTHOR_ROLE="Your Role" \
#   AUTHOR_CONTACT="your-website.com" \
#   ./create-overlay-image.sh "Quote text" output.png
# Confirmed working: 2026-03-27
# Updated: 2026-04-30 (v2.0 - flexible configuration)

# Configuration (with defaults)
PICS_DIR="${PICS_DIR:-/Users/quocmodoro/TinClaw/Pics}"
AUTHOR_NAME="${AUTHOR_NAME:-QUOC MODORO}"
AUTHOR_ROLE="${AUTHOR_ROLE:-CEO & FOUNDER — MODORO | YBAI}"
AUTHOR_CONTACT="${AUTHOR_CONTACT:-lebaoquoc.com}"

# Parameters
OUTPUT="${2:-/tmp/openclaw/uploads/overlay-output.png}"
QUOTE="${1:-Build for trust first. The revenue follows.}"

# Dimensions
WIDTH=1200
HEIGHT=630
MARGIN=60
QUOTE_W=$((WIDTH - MARGIN * 2))  # 1080px — lề trái = phải = 60px

# Step 1: Random chọn 1 ảnh JPG (bỏ qua HEIC)
PICS=($(ls "${PICS_DIR}"/*.JPG 2>/dev/null))
COUNT=${#PICS[@]}
if [ $COUNT -eq 0 ]; then
  echo "ERROR: No JPG files in ${PICS_DIR}"
  exit 1
fi
RANDOM_INDEX=$((RANDOM % COUNT))
CHOSEN_PIC="${PICS[$RANDOM_INDEX]}"
echo "Using photo: $(basename ${CHOSEN_PIC})"

# Step 2: Resize ảnh gốc về 1200px width trước (chuẩn hóa kích thước)
# sau đó crop center về đúng 1200x630
magick "${CHOSEN_PIC}" \
  -resize "${WIDTH}x" \
  -resize "${WIDTH}x${HEIGHT}^" \
  -gravity center \
  -extent "${WIDTH}x${HEIGHT}" \
  /tmp/oc-bg-resized.png

# Step 3: Gradient từ trên trong suốt → dưới tối
magick -size ${WIDTH}x${HEIGHT} gradient:"rgba(0,0,0,0)-rgba(0,0,0,0.88)" \
  /tmp/oc-gradient-bottom.png

magick /tmp/oc-bg-resized.png /tmp/oc-gradient-bottom.png -composite /tmp/oc-bg-gradient.png

# Step 4: Quote text box — 1080px wide, 160px tall
magick -background none -fill white \
  -font "/Users/quocmodoro/Library/Fonts/Anton-Regular.ttf" \
  -pointsize 50 -size ${QUOTE_W}x160 \
  caption:"${QUOTE}" /tmp/oc-quote-text.png

# Step 5: Compose — layout từ bottom:
# 36px  AUTHOR_CONTACT
# 62px  AUTHOR_ROLE
# 100px AUTHOR_NAME
# 150px quote box bottom edge (= 100 + 34px name height + 16px gap)
magick /tmp/oc-bg-gradient.png \
  /tmp/oc-quote-text.png -gravity southwest -geometry +${MARGIN}+150 -composite \
  -font "/System/Library/Fonts/Supplemental/Arial Bold.ttf" \
  -fill white -pointsize 34 \
  -gravity southwest -annotate +${MARGIN}+100 "${AUTHOR_NAME}" \
  -font "/System/Library/Fonts/Supplemental/Arial.ttf" \
  -fill "rgba(255,255,255,0.85)" -pointsize 21 \
  -gravity southwest -annotate +${MARGIN}+62 "${AUTHOR_ROLE}" \
  -fill "rgba(255,255,255,0.6)" -pointsize 19 \
  -gravity southwest -annotate +${MARGIN}+36 "${AUTHOR_CONTACT}" \
  -quality 95 "${OUTPUT}"

# Cleanup
rm -f /tmp/oc-bg-resized.png /tmp/oc-bg-gradient.png /tmp/oc-quote-text.png /tmp/oc-gradient-bottom.png

echo "Created: ${OUTPUT}"
echo "Photo used: $(basename ${CHOSEN_PIC})"
echo "Author: ${AUTHOR_NAME}"
echo "Role: ${AUTHOR_ROLE}"
echo "Contact: ${AUTHOR_CONTACT}"
