# NestJS Request Lifecycle

## Execution Order
```
Incoming Request
  → Middleware (global → module-bound)
    → Guards (global → controller → route)
      → Interceptors pre-handler (global → controller → route)
        → Pipes (global → controller → route → param-level)
          → Route Handler
        → Interceptors post-handler (route → controller → global)
      → Exception Filters (route → controller → global)
Response
```
Each layer has a distinct responsibility. Misplacing logic in the wrong layer is a common NestJS mistake.

## Middleware
```typescript
// Function middleware (simple)
export function logger(req: Request, res: Response, next: NextFunction) {
  console.log(`${req.method} ${req.url}`);
  next(); // ⚠️ forgetting next() hangs the request
}

// Class middleware (with DI)
@Injectable()
export class AuthMiddleware implements NestMiddleware {
  constructor(private authService: AuthService) {}
  use(req: Request, res: Response, next: NextFunction) {
    // can inject services — advantage over function middleware
    next();
  }
}

// Register in module
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(AuthMiddleware)
      .exclude({ path: 'health', method: RequestMethod.GET })
      .forRoutes('*');
  }
}
```
- Middleware runs BEFORE guards — use for raw request mutation (parsing, CORS, logging)
- Cannot access the route handler or which controller will run (no `ExecutionContext`)
- Express middleware works directly; Fastify middleware does NOT — use Fastify hooks instead

## Guards
```typescript
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<Role[]>('roles', [
      context.getHandler(),
      context.getClass(),
    ]);
    if (!requiredRoles) return true;

    const request = context.switchToHttp().getRequest();
    const user = request.user;
    return requiredRoles.some(role => user.roles?.includes(role));
  }
}
```
- Return `true` → proceed, `false` → `ForbiddenException` (403)
- Throw specific exception for custom error messages: `throw new UnauthorizedException('Token expired')`
- Has `ExecutionContext` — knows which controller/handler will run
- Use `@SetMetadata()` + `Reflector` to read decorator metadata

### Guard Binding
```typescript
// Route level
@UseGuards(AuthGuard)
@Get('profile')
getProfile() {}

// Controller level
@UseGuards(AuthGuard)
@Controller('admin')
export class AdminController {}

// Global
app.useGlobalGuards(new AuthGuard()); // ❌ no DI
// ✅ Global with DI:
@Module({
  providers: [{ provide: APP_GUARD, useClass: AuthGuard }],
})
export class AppModule {}
```

## Interceptors
```typescript
@Injectable()
export class TransformInterceptor<T> implements NestInterceptor<T, Response<T>> {
  intercept(context: ExecutionContext, next: CallHandler): Observable<Response<T>> {
    const now = Date.now();
    return next.handle().pipe(
      map(data => ({
        data,
        statusCode: context.switchToHttp().getResponse().statusCode,
        timestamp: new Date().toISOString(),
      })),
      tap(() => console.log(`${Date.now() - now}ms`)),
    );
  }
}
```
- Runs BEFORE and AFTER handler (wraps the handler via RxJS)
- `next.handle()` returns Observable of handler's return value
- Use for: response transformation, caching, logging, timeout
- Can completely override the response or short-circuit with `of(cachedValue)`

### Timeout Interceptor
```typescript
@Injectable()
export class TimeoutInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler) {
    return next.handle().pipe(
      timeout(5000),
      catchError(err => {
        if (err instanceof TimeoutError) {
          throw new RequestTimeoutException();
        }
        throw err;
      }),
    );
  }
}
```

## Pipes
```typescript
// Built-in pipes: ValidationPipe, ParseIntPipe, ParseBoolPipe,
// ParseArrayPipe, ParseUUIDPipe, ParseEnumPipe, DefaultValuePipe

// Param-level
@Get(':id')
findOne(@Param('id', ParseIntPipe) id: number) {} // '123' → 123, 'abc' → 400

// Global validation
app.useGlobalPipes(new ValidationPipe({
  whitelist: true,         // strip unknown properties
  forbidNonWhitelisted: true, // throw on unknown properties
  transform: true,         // auto-transform payloads to DTO instances
  transformOptions: { enableImplicitConversion: true },
}));
```
- Pipes run AFTER guards but BEFORE handler — for validation and transformation
- `transform: true` auto-converts query params from strings to expected types

## Exception Filters
```typescript
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const status = exception.getStatus();

    response.status(status).json({
      statusCode: status,
      message: exception.message,
      timestamp: new Date().toISOString(),
      path: ctx.getRequest<Request>().url,
    });
  }
}

// Catch everything
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    // handle non-HTTP exceptions (TypeORM errors, etc.)
  }
}
```
- Bind with `@UseFilters()` at route/controller level or globally
- Multiple `@Catch(TypeA, TypeB)` — one filter handles several exception types
- Filters catch exceptions thrown from guards, interceptors, pipes, and handlers

## Common Traps

- **Middleware can't use `ExecutionContext`** — if you need to know the route handler, use a guard or interceptor
- **Guard returns `false` with no message** — user gets generic 403, throw `ForbiddenException('reason')` instead
- **Interceptor `next.handle()` not called** — handler never executes, request hangs or returns interceptor's value
- **Pipe validation errors swallowed** — if `exceptionFactory` is misconfigured, errors become 500 instead of 400
- **Exception filter scope** — route-level filter only catches that route; controller-level catches all routes in controller; global catches everything
- **Global providers without DI** — `app.useGlobalGuards(new Guard())` doesn't inject dependencies; use `APP_GUARD`/`APP_PIPE`/`APP_FILTER`/`APP_INTERCEPTOR` provider tokens instead
