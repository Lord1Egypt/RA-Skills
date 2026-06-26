/**
 * Safe output functions that avoid libuv handle closing assertion on Windows.
 * We avoid process.exit() and instead set process.exitCode.
 * This allows Node to cleanly drain stdout before exiting.
 */
function ok(data) {
  const output = JSON.stringify({ success: true, data }, null, 2) + '\n';
  process.stdout.write(output);
  process.exitCode = 0;
}

function err(message, code = 'ERROR') {
  const output = JSON.stringify({ success: false, error: { code, message } }, null, 2) + '\n';
  process.stdout.write(output);
  process.exitCode = 1;
}

/**
 * Removes internal MongoDB fields from objects or arrays of objects.
 * Used to keep public JSON output clean.
 */
function stripMongoFields(input) {
  if (Array.isArray(input)) {
    return input.map(item => stripMongoFields(item));
  }
  if (input && typeof input === 'object') {
    const { _id, __v, ...rest } = input;
    // Also recursively clean nested arrays/objects if needed (e.g. trades)
    Object.keys(rest).forEach(key => {
      if (Array.isArray(rest[key]) || (rest[key] && typeof rest[key] === 'object')) {
        rest[key] = stripMongoFields(rest[key]);
      }
    });
    return rest;
  }
  return input;
}

module.exports = { ok, err, stripMongoFields };
