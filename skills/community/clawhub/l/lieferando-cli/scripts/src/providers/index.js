import { createLieferandoProvider } from './lieferando.js';
import { createUberEatsProvider } from './ubereats.js';
import { assertProvider } from './provider.js';
import { CliError, CODES } from '../errors.js';

const FACTORIES = {
  lieferando: createLieferandoProvider,
  ubereats: createUberEatsProvider,
};

export function createProvider(name, deps) {
  const factory = FACTORIES[name];
  if (!factory) {
    throw new CliError(CODES.INVALID_ARGUMENT, `Unknown provider "${name}". Available: ${Object.keys(FACTORIES).join(', ')}.`, {
      exitCode: 2,
    });
  }
  return assertProvider(factory(deps));
}

export const PROVIDERS = Object.keys(FACTORIES);
