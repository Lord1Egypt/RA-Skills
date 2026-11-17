const fs = require("fs");
const path = require("path");

let cachedName = null;
function skillName() {
  if (cachedName) return cachedName;
  const pkgPath = path.join(
    path.dirname(__filename),
    "..",
    "..",
    "package.json",
  );
  const pkg = JSON.parse(fs.readFileSync(pkgPath, "utf-8"));
  cachedName = pkg.name;
  return cachedName;
}

module.exports = {
  skillName,
};
