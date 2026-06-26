import { defineChannelPluginEntry } from "openclaw/plugin-sdk/core";
import { zulipPlugin } from "./channel-plugin-api.js";
import { setZulipRuntime } from "./src/runtime.js";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const entry: any = defineChannelPluginEntry({
  id: "zulip",
  name: "Zulip",
  description: "Zulip channel plugin — topic threading, metadata DB, bot commands",
  plugin: zulipPlugin,
  setRuntime: setZulipRuntime,
});

export default entry;
