import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { Type } from "@sinclair/typebox";

export default definePluginEntry({
  id: "hello-world",
  name: "Hello World",
  description: "A minimal hello-world plugin for OpenClaw.",
  register(api) {
    api.registerTool({
      name: "hello",
      description: "Returns a hello-world greeting.",
      parameters: Type.Object({
        name: Type.Optional(
          Type.String({ description: "Who to greet. Defaults to 'world'." }),
        ),
      }),
      async execute(_id, params) {
        const who = params.name?.trim() || "world";
        return {
          content: [{ type: "text", text: `Hello, ${who}!` }],
        };
      },
    });
  },
});
