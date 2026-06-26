const { execFileSync } = require("child_process");

function ffprobeDurationMs(filePath) {
  const output = execFileSync(
    "ffprobe",
    [
      "-v",
      "error",
      "-show_entries",
      "format=duration",
      "-of",
      "default=noprint_wrappers=1:nokey=1",
      filePath
    ],
    { encoding: "utf8" }
  ).trim();

  const seconds = Number(output);
  if (!Number.isFinite(seconds) || seconds <= 0) {
    throw new Error(`Failed to probe audio duration for ${filePath}`);
  }

  return Math.round(seconds * 1000);
}

module.exports = {
  ffprobeDurationMs
};
