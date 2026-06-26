export class EdictBudgetExceededError extends Error {
  readonly budget: number;
  readonly current: number;

  constructor(budget: number, current: number) {
    super(`Token budget exceeded: ${current} tokens used, budget is ${budget}`);
    this.name = 'EdictBudgetExceededError';
    this.budget = budget;
    this.current = current;
  }
}

export class EdictCountLimitError extends Error {
  readonly limit: number;
  readonly current: number;

  constructor(limit: number, current: number) {
    super(`Edict count limit exceeded: ${current} edicts present, limit is ${limit}`);
    this.name = 'EdictCountLimitError';
    this.limit = limit;
    this.current = current;
  }
}

export class EdictConflictError extends Error {
  readonly expectedHash: string;
  readonly actualHash: string;

  constructor(expectedHash: string, actualHash: string) {
    super(
      `File was modified since last load. Expected hash ${expectedHash}, found ${actualHash}. Reload and retry.`
    );
    this.name = 'EdictConflictError';
    this.expectedHash = expectedHash;
    this.actualHash = actualHash;
  }
}

export class EdictCategoryError extends Error {
  readonly category: string;
  readonly validCategories: string[];

  constructor(category: string, validCategories: string[]) {
    super(
      `Unknown category "${category}". Valid categories: ${validCategories.join(', ')}`
    );
    this.name = 'EdictCategoryError';
    this.category = category;
    this.validCategories = validCategories;
  }
}

export class EdictValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'EdictValidationError';
  }
}

export class EdictNotFoundError extends Error {
  readonly edictId: string;

  constructor(id: string) {
    super(`Edict not found: "${id}"`);
    this.name = 'EdictNotFoundError';
    this.edictId = id;
  }
}
