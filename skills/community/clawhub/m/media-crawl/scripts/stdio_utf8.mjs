/**
 * 统一的 UTF-8 文本输出。
 * - TTY：直接写字符串，让 Node 走平台原生终端路径（Windows 下可避免中文乱码）。
 * - Pipe/File：写 UTF-8 bytes，确保跨进程与重定向一致。
 * @param {NodeJS.WriteStream} stream
 * @param {string} text
 */
function writeLine(stream, text) {
  const line = `${text}\n`;
  if (stream.isTTY) {
    stream.write(line);
    return;
  }
  stream.write(Buffer.from(line, "utf8"));
}

/** @param {string} text */
export function print(text) {
  writeLine(process.stdout, String(text));
}

/** @param {string} text */
export function print_error(text) {
  writeLine(process.stderr, String(text));
}
