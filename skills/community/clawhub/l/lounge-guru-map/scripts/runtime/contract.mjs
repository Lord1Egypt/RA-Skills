import { z } from 'zod';

export const MAX_QUERY_LENGTH = 120;
export const MAX_PAGE_SIZE = 25;
export const MAX_TYPE_FILTERS = 5;
export const MAX_FACILITY_FILTERS = 8;

const PlainTextQuerySchema = z
  .string()
  .trim()
  .min(1)
  .max(MAX_QUERY_LENGTH)
  .refine((value) => !/[\u0000-\u001f\u007f]/u.test(value), 'Use plain text only.')
  .refine((value) => !/[`{}<>\\]/u.test(value), 'Use plain text only.');

const OptionalPlainTextSchema = PlainTextQuerySchema.optional();

const CursorSchema = z
  .string()
  .trim()
  .regex(/^\d+$/, 'Cursor must be a numeric offset.')
  .optional();

const OptionalExactMatchSchema = z.string().trim().min(1).max(80).optional();

export const SearchLoungesInputSchema = z
  .object({
    query: OptionalPlainTextSchema,
    airportCode: z
      .string()
      .trim()
      .toUpperCase()
      .regex(/^[A-Z0-9]{3}$/, 'Airport code must be a 3-character IATA code.')
      .optional(),
    country: OptionalExactMatchSchema,
    city: OptionalExactMatchSchema,
    types: z.array(z.string().trim().min(1).max(24)).max(MAX_TYPE_FILTERS).optional(),
    facilities: z.array(z.string().trim().min(1).max(80)).max(MAX_FACILITY_FILTERS).optional(),
    limit: z.number().int().min(1).max(MAX_PAGE_SIZE).optional(),
    cursor: CursorSchema,
  })
  .strict();

export const LoungeSummarySchema = z.object({
  id: z.string(),
  airportCode: z.string(),
  airportName: z.string(),
  country: z.string(),
  city: z.string(),
  type: z.string(),
  terminal: z.string(),
  name: z.string(),
  facilities: z.array(z.string()),
  location: z.string(),
  lat: z.number(),
  lon: z.number(),
});

export const LoungeDetailSchema = LoungeSummarySchema.extend({
  openingHours: z.string(),
  conditions: z.array(z.string()),
  url: z.string(),
  slug: z.string(),
});

export const SearchLoungesOutputSchema = z.object({
  totalMatches: z.number().int().nonnegative(),
  nextCursor: z.string().nullable(),
  results: z.array(LoungeSummarySchema),
});

export const GetLoungeInputSchema = z
  .object({
    id: z.string().trim().min(1).max(120),
  })
  .strict();

export const GetLoungeOutputSchema = z.object({
  lounge: LoungeDetailSchema,
});

export const CatalogMetaOutputSchema = z.object({
  generatedAt: z.string(),
  sourceFile: z.string(),
  stats: z.object({
    totalInputRows: z.number().int().nonnegative(),
    totalFeatures: z.number().int().nonnegative(),
    droppedRows: z.number().int().nonnegative(),
    uniqueAirports: z.number().int().nonnegative(),
    uniqueCountries: z.number().int().nonnegative(),
    uniqueCities: z.number().int().nonnegative(),
  }),
  filters: z.object({
    types: z.array(z.string()),
    countries: z.array(z.string()),
    cities: z.array(z.string()),
    facilities: z.array(z.string()),
  }),
});

export const AirportPromptArgsSchema = {
  airportCode: z
    .string()
    .trim()
    .toUpperCase()
    .regex(/^[A-Z0-9]{3}$/),
};

export const ComparePromptArgsSchema = {
  airportCode: z
    .string()
    .trim()
    .toUpperCase()
    .regex(/^[A-Z0-9]{3}$/),
  type: z.string().trim().min(1).max(24).optional(),
};
