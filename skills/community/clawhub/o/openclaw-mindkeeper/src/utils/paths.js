import path from "node:path";

export function appendSuffixToPath(filePath, suffix) {
  const parsed = path.parse(filePath);
  return path.join(parsed.dir, `${parsed.name}-${suffix}${parsed.ext}`);
}
