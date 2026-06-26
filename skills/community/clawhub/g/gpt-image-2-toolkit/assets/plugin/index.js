import { t as definePluginEntry } from "../../plugin-entry-CK-4XWE0.js";
import { buildHnbcImageGenerationProvider } from "./image-generation-provider.js";

var hnbc_default = definePluginEntry({
  id: "hnbc",
  name: "HNBC Provider",
  description: "Bundled HNBC image generation provider",
  register(api) {
    api.registerImageGenerationProvider(buildHnbcImageGenerationProvider());
  }
});

export { hnbc_default as default };
