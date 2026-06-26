import type { CommandDef } from "../lib/types.ts";
import { checkLegacySuccess, getLegacyErrorMessage } from "../lib/types.ts";

function validateLatLng(value: string): string | null {
  const parts = value.split(",");
  if (parts.length !== 2) {
    return "must be in <lat,lng> format";
  }
  const lat = Number(parts[0]?.trim());
  const lng = Number(parts[1]?.trim());
  if (!Number.isFinite(lat) || !Number.isFinite(lng)) {
    return "must contain valid numbers";
  }
  if (lat < -90 || lat > 90 || lng < -180 || lng > 180) {
    return "latitude must be -90..90, longitude must be -180..180";
  }
  return null;
}

const reverseGeocode: CommandDef = {
  name: "reverse-geocode",
  description: "Convert coordinates to a human-readable address.",
  usage: "reverse-geocode --latlng <lat,lng>",
  method: "GET",
  url: "https://maps.googleapis.com/maps/api/geocode/json",
  auth: "query",
  flags: {
    latlng: {
      description: "Latitude,longitude pair",
      required: true,
      placeholder: "<lat,lng>",
      validate: validateLatLng,
    },
  },
  buildRequest: (flags) => ({
    params: { latlng: flags.latlng! },
  }),
  checkSuccess: checkLegacySuccess,
  getErrorMessage: getLegacyErrorMessage,
};

export default reverseGeocode;
