import type { CommandDef } from "../lib/types.ts";
import { checkLegacySuccess, getLegacyErrorMessage } from "../lib/types.ts";

function validateLocations(value: string): string | null {
  const points = value.split("|");
  for (const point of points) {
    const parts = point.trim().split(",");
    if (parts.length !== 2) {
      return "each point must be in <lat,lng> format, separated by |";
    }
    const lat = Number(parts[0]?.trim());
    const lng = Number(parts[1]?.trim());
    if (!Number.isFinite(lat) || !Number.isFinite(lng)) {
      return "each point must contain valid numbers";
    }
    if (lat < -90 || lat > 90 || lng < -180 || lng > 180) {
      return "latitude must be -90..90, longitude must be -180..180";
    }
  }
  return null;
}

const elevation: CommandDef = {
  name: "elevation",
  description: "Get elevation data for locations on the earth.",
  usage: "elevation --locations <lat,lng|lat,lng|...>",
  method: "GET",
  url: "https://maps.googleapis.com/maps/api/elevation/json",
  auth: "query",
  flags: {
    locations: {
      description: "Pipe-separated lat,lng pairs",
      required: true,
      placeholder: "<lat,lng|lat,lng|...>",
      validate: validateLocations,
    },
  },
  buildRequest: (flags) => ({
    params: { locations: flags.locations! },
  }),
  checkSuccess: checkLegacySuccess,
  getErrorMessage: getLegacyErrorMessage,
};

export default elevation;
