export type MaskRegion = {
  x: number;
  y: number;
  w: number;
  h: number;
};

function isFiniteNumber(value: number): boolean {
  return Number.isFinite(value);
}

export function parseMaskRegions(mask: string): MaskRegion[] {
  const regions = mask
    .split(";")
    .map((region) => region.trim())
    .filter((region) => region.length > 0)
    .map((region, index) => {
      const parts = region.split(",").map((part) => Number(part.trim()));
      if (parts.length !== 4 || parts.some((part) => !isFiniteNumber(part))) {
        throw new Error(
          `Invalid --mask region #${index + 1}: expected x,y,w,h. / 无效的 --mask 第 ${index + 1} 个区域：应为 x,y,w,h。`,
        );
      }

      const [x, y, w, h] = parts;
      if (x < 0 || y < 0 || w <= 0 || h <= 0) {
        throw new Error(
          `Invalid --mask region #${index + 1}: x and y must be >= 0, w and h must be > 0. / 无效的 --mask 第 ${index + 1} 个区域：x 和 y 必须 >= 0，w 和 h 必须 > 0。`,
        );
      }

      return { x, y, w, h };
    });

  if (regions.length === 0) {
    throw new Error("Invalid --mask value: provide at least one region. / 无效的 --mask 值：请至少提供一个区域。");
  }

  return regions;
}

export function pointInMaskRegion(x: number, y: number, regions: MaskRegion[]): boolean {
  return regions.some((region) => x >= region.x && x < region.x + region.w && y >= region.y && y < region.y + region.h);
}
