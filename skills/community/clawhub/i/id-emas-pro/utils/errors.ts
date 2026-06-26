/**
 * Error handling utilities
 */

export class EmasProError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500,
    public retryable: boolean = false
  ) {
    super(message);
    this.name = 'EmasProError';
  }
}

export class ScrapingError extends EmasProError {
  constructor(message: string, brand: string) {
    super(
      `Failed to scrape ${brand}: ${message}`,
      'SCRAPING_FAILED',
      503,
      true
    );
    this.name = 'ScrapingError';
  }
}

export class StorageError extends EmasProError {
  constructor(message: string) {
    super(
      `Storage error: ${message}`,
      'STORAGE_ERROR',
      500,
      false
    );
    this.name = 'StorageError';
  }
}

export class ValidationError extends EmasProError {
  constructor(message: string) {
    super(
      `Validation error: ${message}`,
      'VALIDATION_ERROR',
      400,
      false
    );
    this.name = 'ValidationError';
  }
}

export class TierError extends EmasProError {
  constructor(feature: string, requiredTier: string) {
    super(
      `Feature '${feature}' requires ${requiredTier} tier`,
      'TIER_INSUFFICIENT',
      403,
      false
    );
    this.name = 'TierError';
  }
}

export class AIError extends EmasProError {
  constructor(message: string) {
    super(
      `AI analysis error: ${message}`,
      'AI_ERROR',
      502,
      true
    );
    this.name = 'AIError';
  }
}

/**
 * Handle error and return user-friendly message
 */
export function handleError(error: unknown): string {
  if (error instanceof EmasProError) {
    switch (error.code) {
      case 'SCRAPING_FAILED':
        return `❌ Gagal mengambil data: ${error.message}\n\nCoba lagi nanti atau periksa koneksi internet.`;
      
      case 'STORAGE_ERROR':
        return `⚠️ Gagal menyimpan data. Fitur mungkin tidak berfungsi dengan baik.`;
      
      case 'VALIDATION_ERROR':
        return `⚠️ ${error.message}`;
      
      case 'TIER_INSUFFICIENT':
        return `🔒 ${error.message}\n\nUpgrade tier untuk mengakses fitur ini.`;
      
      case 'AI_ERROR':
        return `🤖 Analisis AI gagal: ${error.message}\n\nCoba lagi nanti.`;
      
      default:
        return `❌ Terjadi kesalahan: ${error.message}`;
    }
  }

  if (error instanceof Error) {
    return `❌ Error: ${error.message}`;
  }

  return '❌ Terjadi kesalahan yang tidak diketahui.';
}

/**
 * Wrap async function with error handling
 */
export function withErrorHandling<T>(
  fn: () => Promise<T>,
  fallback?: T
): Promise<T | undefined> {
  return fn().catch((error) => {
    console.error('Error caught:', error);
    return fallback;
  });
}
