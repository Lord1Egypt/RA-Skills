import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

export async function writeOutputFile(targetPath, content) {
  const directory = path.dirname(targetPath);
  await mkdir(directory, { recursive: true });
  await writeFile(targetPath, content, "utf8");
}
