import type { EdictFileSchema } from '../types.js';

export const DEFAULT_SCHEMA: EdictFileSchema = {
  version: 1,
  config: {
    maxEdicts: 200,
    tokenBudget: 4000,
    categories: [],
  },
  edicts: [],
  history: [],
};

/**
 * Abstract storage interface for reading/writing edict files.
 */
export interface Storage {
  read(): Promise<EdictFileSchema>;
  write(data: EdictFileSchema): Promise<void>;
  hash(): Promise<string | null>;
  exists(): Promise<boolean>;
}
