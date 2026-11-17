/**
 * GCJ-02 (Chinese encrypted coords, used by domestic map providers) <-> WGS-84 (GPS/OSM).
 *
 * The GCJ-02 offset is a non-invertible transform; the iterative inverse
 * below converges to well under a centimeter in 3 iterations, versus a
 * 100-600m error if GCJ-02 coordinates are used as WGS-84 directly.
 *
 * Reference: the widely used "eviltransform" algorithm.
 */
const PI = Math.PI;
const SEMI_AXIS = 6378245.0;
const EE = 0.00669342162296594323;

function outOfChina(lng, lat) {
  return !(lng > 73.66 && lng < 135.05 && lat > 3.86 && lat < 53.55);
}

function transformLat(x, y) {
  let ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * Math.sqrt(Math.abs(x));
  ret += (20.0 * Math.sin(6.0 * x * PI) + 20.0 * Math.sin(2.0 * x * PI)) * 2.0 / 3.0;
  ret += (20.0 * Math.sin(y * PI) + 40.0 * Math.sin(y / 3.0 * PI)) * 2.0 / 3.0;
  ret += (160.0 * Math.sin(y / 12.0 * PI) + 320.0 * Math.sin(y * PI / 30.0)) * 2.0 / 3.0;
  return ret;
}

function transformLng(x, y) {
  let ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * Math.sqrt(Math.abs(x));
  ret += (20.0 * Math.sin(6.0 * x * PI) + 20.0 * Math.sin(2.0 * x * PI)) * 2.0 / 3.0;
  ret += (20.0 * Math.sin(x * PI) + 40.0 * Math.sin(x / 3.0 * PI)) * 2.0 / 3.0;
  ret += (150.0 * Math.sin(x / 12.0 * PI) + 300.0 * Math.sin(x / 30.0 * PI)) * 2.0 / 3.0;
  return ret;
}

/** WGS-84 -> GCJ-02 (exact forward transform). Identity outside China. */
function wgs84ToGcj02(lng, lat) {
  if (outOfChina(lng, lat)) return [lng, lat];
  let dLat = transformLat(lng - 105.0, lat - 35.0);
  let dLng = transformLng(lng - 105.0, lat - 35.0);
  const radLat = (lat / 180.0) * PI;
  let magic = Math.sin(radLat);
  magic = 1 - EE * magic * magic;
  const sqrtMagic = Math.sqrt(magic);
  dLat = (dLat * 180.0) / (((SEMI_AXIS * (1 - EE)) / (magic * sqrtMagic)) * PI);
  dLng = (dLng * 180.0) / ((SEMI_AXIS / sqrtMagic) * Math.cos(radLat) * PI);
  return [lng + dLng, lat + dLat];
}

/** GCJ-02 -> WGS-84 (iterative inverse; error < 1cm after 3 rounds). */
function gcj02ToWgs84(lng, lat) {
  if (outOfChina(lng, lat)) return [lng, lat];
  let wgsLng = lng;
  let wgsLat = lat;
  for (let i = 0; i < 3; i++) {
    const [gLng, gLat] = wgs84ToGcj02(wgsLng, wgsLat);
    wgsLng += lng - gLng;
    wgsLat += lat - gLat;
  }
  return [wgsLng, wgsLat];
}

module.exports = { wgs84ToGcj02, gcj02ToWgs84 };
