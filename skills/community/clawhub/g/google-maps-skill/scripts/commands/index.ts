import type { CommandDef } from "../lib/types.ts";
import geocode from "./geocode.ts";
import reverseGeocode from "./reverse-geocode.ts";
import directions from "./directions.ts";
import placesSearch from "./places-search.ts";
import placesNearby from "./places-nearby.ts";
import placeDetail from "./place-detail.ts";
import elevation from "./elevation.ts";
import timezone from "./timezone.ts";

export const COMMAND_ORDER: CommandDef[] = [
  geocode,
  reverseGeocode,
  directions,
  placesSearch,
  placesNearby,
  placeDetail,
  elevation,
  timezone,
];

export const COMMAND_REGISTRY = new Map<string, CommandDef>(
  COMMAND_ORDER.map((cmd) => [cmd.name, cmd]),
);
