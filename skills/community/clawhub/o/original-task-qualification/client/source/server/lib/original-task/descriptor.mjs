import { existsSync, readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

export const ORIGINAL_TASK_DESCRIPTOR_PATH = "/discovery/original-task-correspondence.json";
export const ORIGINAL_TASK_CLIENT_ARCHIVE_PATH = "/for-agents/original-task/original-task-client.tar.gz";

const published = fileURLToPath(new URL("../../../client/public/discovery/original-task-correspondence.json", import.meta.url));
const bundled = fileURLToPath(new URL("./bundled-descriptor.json", import.meta.url));
const archiveFile = fileURLToPath(new URL(`../../../client/public${ORIGINAL_TASK_CLIENT_ARCHIVE_PATH}`, import.meta.url));

export function originalTaskClientArchiveFile() {
  return archiveFile;
}

export function originalTaskDescriptor() {
  const source = existsSync(published) ? published : bundled;
  return JSON.parse(readFileSync(source, "utf8"));
}
