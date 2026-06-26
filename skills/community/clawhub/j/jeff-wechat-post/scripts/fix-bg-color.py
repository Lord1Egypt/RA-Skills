"""Post-process KIE image: replace near-black background with navy blue."""
import sys
from PIL import Image
import numpy as np

def replace_black_bg(img_path, output_path, bg_color=(26, 42, 74), threshold=30):
    img = Image.open(img_path).convert("RGB")
    arr = np.array(img)
    # Find near-black pixels (all channels < threshold)
    mask = (arr[:,:,0] < threshold) & (arr[:,:,1] < threshold) & (arr[:,:,2] < threshold)
    # Replace with navy
    arr[mask] = bg_color
    Image.fromarray(arr).save(output_path)
    print(f"Done: {output_path}")

if __name__ == "__main__":
    replace_black_bg(sys.argv[1], sys.argv[2])
