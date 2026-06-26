import type { CommandDef } from "../lib/types.ts";
import { checkNewApiSuccess, getNewApiErrorMessage } from "../lib/types.ts";

const placeDetail: CommandDef = {
  name: "place-detail",
  description: "Get detailed information about a specific place by its place ID.",
  usage: "place-detail --place-id <id>",
  method: "GET",
  url: "https://places.googleapis.com/v1/places",
  auth: "header",
  fieldMask: "id,displayName,formattedAddress,location,rating,websiteUri,nationalPhoneNumber,regularOpeningHours,types,editorialSummary",
  flags: {
    "place-id": {
      description: "Google Maps place ID",
      required: true,
      placeholder: "<id>",
    },
  },
  buildUrl: (flags) => `https://places.googleapis.com/v1/places/${flags["place-id"]}`,
  buildRequest: () => ({}),
  checkSuccess: checkNewApiSuccess,
  getErrorMessage: getNewApiErrorMessage,
};

export default placeDetail;
