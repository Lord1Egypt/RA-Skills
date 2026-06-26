import { readFile } from "fs/promises";

export async function loadCatalogTextFromFile(csvPath) {
  return readFile(csvPath, "utf-8");
}
