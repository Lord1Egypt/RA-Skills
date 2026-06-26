import { readFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

export interface CliMeta {
  skillVersion: string;
  skillName: string;
}

export function loadCliMeta(): CliMeta {
  const __dirname = dirname(fileURLToPath(import.meta.url));
  const pkgPath = resolve(__dirname, "../../package.json");
  const pkg = JSON.parse(readFileSync(pkgPath, "utf8")) as {
    name?: string;
    version?: string;
  };
  return {
    skillVersion: pkg.version || "0.0.0",
    skillName: pkg.name || "@lista-dao/lista-wallet-connect-skill",
  };
}
