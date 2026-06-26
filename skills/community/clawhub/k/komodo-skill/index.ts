import { komodo } from "./openclaw.ts";

const version = await komodo.core_version();
console.log("Komodo Core version:", version);
