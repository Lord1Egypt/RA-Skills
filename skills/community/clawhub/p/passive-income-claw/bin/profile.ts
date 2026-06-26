#!/usr/bin/env node
import {
  readProfile, getField, setField, writeProfile, profileDump, resetDaily,
  utcDate, die, out, main,
} from "./lib.ts";

const commands: Record<string, (argv: string[]) => void> = {
  get: (argv) => {
    const key = argv.find((a) => !a.startsWith("--")) || (argv.includes("--key") ? argv[argv.indexOf("--key") + 1] : undefined);
    if (!key) die("Usage: profile.ts get <key>");
    const content = readProfile();
    const value = getField(content, key);
    if (value === null) die(`Field '${key}' not found`);
    out({ [key]: value });
  },

  set: (argv) => {
    let key: string | undefined;
    let value: string | undefined;

    if (argv.includes("--key")) {
      key = argv[argv.indexOf("--key") + 1];
      value = argv.includes("--value") ? argv[argv.indexOf("--value") + 1] : undefined;
    } else {
      const positional = argv.filter((a) => !a.startsWith("--"));
      key = positional[0];
      value = positional.slice(1).join(" ");
    }

    if (!key) die("Missing key");
    if (!value) die("Missing value");
    let content = readProfile();
    content = setField(content, key, value);
    writeProfile(content);
    out({ updated: true, [key]: value });
  },

  "reset-daily": () => {
    const content = readProfile();
    const { content: newContent, result } = resetDaily(content, utcDate());
    if (result.reset) writeProfile(newContent);
    out(result);
  },

  dump: () => {
    out(profileDump(readProfile()));
  },
};

main(() => {
  const [cmd, ...rest] = process.argv.slice(2);
  if (!cmd || !commands[cmd]) die("Usage: profile.ts <get|set|reset-daily|dump> [args]");
  commands[cmd](rest);
});
