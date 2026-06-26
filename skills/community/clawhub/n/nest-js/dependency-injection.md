# NestJS Dependency Injection

## Provider Types

### Standard (class-based)
```typescript
@Injectable()
export class UsersService {
  constructor(private readonly usersRepo: UsersRepository) {}
}
// Registered as: providers: [UsersService]
// Equivalent to: { provide: UsersService, useClass: UsersService }
```

### Value Provider
```typescript
{ provide: 'API_KEY', useValue: process.env.API_KEY }
// Inject with: @Inject('API_KEY') private apiKey: string
```

### Factory Provider
```typescript
{
  provide: 'ASYNC_CONNECTION',
  useFactory: async (configService: ConfigService) => {
    const dbConfig = configService.get('database');
    return createConnection(dbConfig);
  },
  inject: [ConfigService], // factory dependencies
}
```
- `inject` array matches factory parameter order
- Can be async — Nest waits for resolution before proceeding

### Existing Provider (alias)
```typescript
{ provide: 'AliasedService', useExisting: ConcreteService }
// Both tokens point to same singleton instance
```

## Injection Scopes

### DEFAULT (singleton) — most common
- One instance for entire app lifetime
- Shared across all requests
- ⚠️ Do NOT store request-specific state in singletons

### REQUEST
```typescript
@Injectable({ scope: Scope.REQUEST })
export class RequestScopedService {}
```
- New instance per incoming request
- **Bubbles up**: if A (singleton) depends on B (request-scoped), A becomes request-scoped too
- Performance cost — avoid unless you genuinely need per-request state (multi-tenancy, request context)
- Controllers depending on request-scoped providers also become request-scoped

### TRANSIENT
```typescript
@Injectable({ scope: Scope.TRANSIENT })
export class TransientService {}
```
- New instance per injection (every consumer gets its own)
- Not shared between consumers even in same request

## Common Traps

### Missing `@Injectable()`
```typescript
// ❌ Nest silently can't resolve this
export class MyService {
  constructor(private dep: OtherService) {}
}

// ✅ Decorator is required for metadata emission
@Injectable()
export class MyService {
  constructor(private dep: OtherService) {}
}
```

### Interface Injection (TypeScript interfaces erased at runtime)
```typescript
// ❌ Interfaces don't exist at runtime — Nest can't resolve
constructor(private service: IMyService) {}

// ✅ Use string/symbol token + @Inject
constructor(@Inject('IMyService') private service: IMyService) {}

// ✅ Or use abstract class as token (classes survive compilation)
export abstract class IMyService {
  abstract doThing(): void;
}
```

### Circular Provider Dependencies
```typescript
// ❌ A injects B, B injects A — crash
// ✅ forwardRef on BOTH providers
@Injectable()
export class ServiceA {
  constructor(
    @Inject(forwardRef(() => ServiceB))
    private serviceB: ServiceB,
  ) {}
}

@Injectable()
export class ServiceB {
  constructor(
    @Inject(forwardRef(() => ServiceA))
    private serviceA: ServiceA,
  ) {}
}
```
Better solution: extract shared logic into a third service.

### Optional Dependencies
```typescript
@Injectable()
export class NotificationService {
  constructor(
    @Optional() @Inject('MAILER') private mailer?: MailerService,
  ) {}
  // mailer is undefined if MAILER provider not registered — no crash
}
```

### Custom Provider Tokens
```typescript
// Symbol tokens prevent collision
export const CACHE_MANAGER = Symbol('CACHE_MANAGER');

// Register
{ provide: CACHE_MANAGER, useClass: RedisCacheManager }

// Inject
constructor(@Inject(CACHE_MANAGER) private cache: CacheManager) {}
```

### `ModuleRef` for Dynamic Resolution
```typescript
@Injectable()
export class DynamicService {
  constructor(private moduleRef: ModuleRef) {}

  async getService() {
    // Resolve request-scoped or transient providers dynamically
    const svc = await this.moduleRef.resolve(TransientService);
    // .get() for singletons (synchronous)
    const singleton = this.moduleRef.get(SingletonService);
  }
}
```
