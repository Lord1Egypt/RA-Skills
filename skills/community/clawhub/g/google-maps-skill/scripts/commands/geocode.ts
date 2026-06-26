import type { CommandDef } from "../lib/types.ts";
import { checkLegacySuccess, getLegacyErrorMessage } from "../lib/types.ts";

const geocode: CommandDef = {
  name: "geocode",
  description: "Convert an address to geographic coordinates.",
  usage: "geocode --address <text>",
  method: "GET",
  url: "https://maps.googleapis.com/maps/api/geocode/json",
  auth: "query",
  flags: {
    address: {
      description: "Address to geocode",
      required: true,
      placeholder: "<text>",
    },
  },
  buildRequest: (flags) => ({
    params: { address: flags.address! },
  }),
  checkSuccess: checkLegacySuccess,
  getErrorMessage: getLegacyErrorMessage,
};

export default geocode;
