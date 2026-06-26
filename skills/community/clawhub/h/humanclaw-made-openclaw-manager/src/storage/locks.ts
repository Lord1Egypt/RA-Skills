const queues = new Map<string, Promise<unknown>>();

export const withNamedLock = async <T>(key: string, fn: () => Promise<T>): Promise<T> => {
  const previous = queues.get(key) || Promise.resolve();
  let release: () => void = () => {};
  const current = new Promise<void>((resolve) => {
    release = resolve;
  });

  queues.set(key, previous.finally(() => current));
  await previous;

  try {
    return await fn();
  } finally {
    release();
    if (queues.get(key) === current) {
      queues.delete(key);
    }
  }
};

