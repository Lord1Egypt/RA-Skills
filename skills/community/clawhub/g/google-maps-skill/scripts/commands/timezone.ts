import type { CommandDef } from "../lib/types.ts";
import { checkLegacySuccess, getLegacyErrorMessage } from "../lib/types.ts";

function validateLocation(value: string): string | null {
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

function validateTimestamp(value: string): string | null {
  const num = Number(value);
  if (!Number.isFinite(num) || num < 0) {
    return "must be a non-negative Unix timestamp";
  }
  return null;
}

const timezone: CommandDef = {
  name: "timezone",
  description: "Get timezone information for a location and timestamp.",
  usage: "timezone --location <lat,lng> [--timestamp <unix_seconds>]",
  method: "GET",
  url: "https://maps.googleapis.com/maps/api/timezone/json",
  auth: "query",
  flags: {
    location: {
      description: "Latitude,longitude pair",
      required: true,
      placeholder: "<lat,lng>",
      validate: validateLocation,
    },
    timestamp: {
      description: "Unix timestamp (defaults to current time)",
      required: false,
      placeholder: "<unix_seconds>",
      validate: validateTimestamp,
    },
  },
  buildRequest: (flags) => ({
    params: {
      location: flags.location!,
      timestamp: flags.timestamp ?? String(Math.floor(Date.now() / 1000)),
    },
  }),
  checkSuccess: checkLegacySuccess,
  getErrorMessage: getLegacyErrorMessage,
};

export default timezone;
