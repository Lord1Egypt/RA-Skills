export function parseDuration(value: string | number): number {
  if (typeof value === 'number') {
    if (!Number.isFinite(value) || value < 0) {
      throw new Error(`Invalid duration "${value}". Must be a non-negative finite number of seconds.`);
    }
    return value;
  }

  const input = value.trim().toLowerCase();
  if (/^\d+$/.test(input)) {
    return Number(input);
  }

  const match = input.match(/^(\d+)([mhd])$/);
  if (!match) {
    throw new Error(
      `Invalid duration "${value}". Use seconds or suffixed values like 30m, 2h, 7d.`
    );
  }

  const amount = Number(match[1]);
  const unit = match[2];
  const factors: Record<string, number> = {
    m: 60,
    h: 3600,
    d: 86400,
  };

  return amount * factors[unit];
}
