---
name: nestjs-dev-guide
description: NestJS Node.js server-side framework development guide.
---

# NestJS Development Guide

NestJS is a progressive framework for building efficient, scalable Node.js server-side applications. Built with TypeScript, it integrates OOP/FP/FRP, uses Express (default) or Fastify under the hood, and its architecture is deeply inspired by Angular.

Version: v11+ | Requires Node.js ≥20

## Trigger Scenarios

Use when the user needs to build a backend application with NestJS, create REST APIs, use decorators and dependency injection, build microservices, configure Swagger documentation, or write NestJS Controllers/Providers/Modules/Guards/Pipes/Interceptors. Trigger keywords include "nest", "nestjs", "create API", "backend service", "decorator injection", "guard", "pipe", "interceptor", "swagger", etc.

## Quick Start

```bash
npm i -g @nestjs/cli
nest new my-project
cd my-project && npm run start:dev
```

Or use `npx @nestjs/cli@latest new my-project` to avoid global installation.

### Project File Structure

```
src/
├── main.ts              # Application entry, NestFactory.create()
├── app.module.ts        # Root module
├── app.controller.ts    # Base controller
├── app.controller.spec.ts
└── app.service.ts       # Base service
```

## Core Concepts

### 1. Module

The `@Module()` decorator defines modules — the logical boundaries and DI container scopes of the application.

```ts
@Module({
  imports: [OtherModule],        // Import other modules
  controllers: [CatsController], // Register controllers
  providers: [CatsService],      // Register providers
  exports: [CatsService],        // Export providers for use by other modules
})
export class CatsModule {}
```

- **Feature modules**: Organized by domain, e.g., `CatsModule`, `UsersModule`
- **Shared modules**: Expose providers via the `exports` array
- **Global modules**: `@Global()` decorator, but **not recommended** to overuse
- **Dynamic modules**: `static forRoot()` returns a runtime-configured module
- **Module re-exporting**: Put imported modules in `exports`

### 2. Controller

`@Controller('prefix')` + HTTP method decorators define routes:

```ts
@Controller('cats')
export class CatsController {
  @Get()        findAll() {}
  @Get(':id')   findOne(@Param('id') id: string) {}
  @Post()       create(@Body() dto: CreateCatDto) {}
  @Put(':id')   update(@Param('id') id: string, @Body() dto: UpdateCatDto) {}
  @Delete(':id') remove(@Param('id') id: string) {}
}
```

**Parameter Decorators Cheat Sheet**:

| Decorator | Extracts |
|---|---|
| `@Param(key?)` | Route parameters |
| `@Body(key?)` | Request body |
| `@Query(key?)` | Query parameters |
| `@Headers(name?)` | Request headers |
| `@Req()` | Native Request object |
| `@Res()` | Native Response (manual management required) |
| `@Ip()` | Client IP |
| `@HostParam()` | Subdomain parameters |

**Route wildcards**: `@Get('ab{*splat}cd')`, `@Get('prefix/*')`

**Status codes and headers**: `@HttpCode(204)`, `@Header('Cache-Control', 'none')`

**Redirect**: `@Redirect('url', 301)` or return `{ url, statusCode }`

**DTO Definition**: Use **class** (not interface), because interfaces disappear after compilation and cannot provide runtime type metadata:
```ts
export class CreateCatDto {
  name: string;
  age: number;
  breed: string;
}
```

### 3. Provider

Classes marked with `@Injectable()`, injected via constructor:

```ts
@Injectable()
export class CatsService {
  private cats: Cat[] = [];
  create(cat: Cat) { this.cats.push(cat); }
  findAll(): Cat[] { return this.cats; }
}

@Controller('cats')
export class CatsController {
  constructor(private catsService: CatsService) {}  // Auto-injected
}
```

**Custom Providers** (using full syntax in `@Module.providers`):

| Syntax | Purpose |
|---|---|
| `{ provide: Token, useClass: Class }` | Standard class provider |
| `{ provide: Token, useValue: value }` | Constant value / mock object |
| `{ provide: Token, useFactory: fn, inject: [...] }` | Factory function |
| `{ provide: Token, useExisting: OtherToken }` | Alias |

**Scope**: Default SINGLETON (application-level singleton), can be set to REQUEST (request-level).

**Optional Providers**: `@Optional()` decorator, no error if dependency is missing.

### 4. Middleware

Plain Express middleware class implementing `NestMiddleware`, bound in consumer:

```ts
@Injectable()
export class LoggerMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) { /* ... */ next(); }
}

// Apply in module
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer.apply(LoggerMiddleware).forRoutes('cats');
  }
}
```

### 5. Pipe — Validation & Transformation

Implements `PipeTransform`, performs validation and/or data transformation. **Execution order**: Middleware → Guards → Interceptor(pre) → Pipe → Handler → Interceptor(post) → Exception Filter.

**Built-in pipes**: `ValidationPipe`, `ParseIntPipe`, `ParseBoolPipe`, `ParseArrayPipe`, `ParseUUIDPipe`

#### ValidationPipe (Recommended)

```bash
npm i class-validator class-transformer
```

```ts
// main.ts — global enable
app.useGlobalPipes(new ValidationPipe({
  whitelist: true,            // Automatically strip undeclared properties
  forbidNonWhitelisted: true, // Error if non-whitelisted properties exist
  transform: true,            // Auto type conversion (string→number etc.)
  disableErrorMessages: false,
}));
```

```ts
// DTO using validation decorators
import { IsString, IsInt, IsEmail, Min, Max } from 'class-validator';

export class CreateUserDto {
  @IsString() @IsNotEmpty()
  name: string;

  @IsInt() @Min(0) @Max(150)
  age: number;

  @IsEmail()
  email: string;
}
```

**Zod validation** alternative:
```ts
const schema = z.object({ name: z.string(), age: z.number() });
@UsePipes(new ZodValidationPipe(schema))
```

### 6. Guard — Authorization Control

Implements `CanActivate`, returns `boolean` determining whether to proceed. Executes after middleware and before interceptors/pipes.

```ts
@Injectable()
export class AuthGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    return validateRequest(request);
  }
}
```

**Role guard + custom metadata**:

```ts
// Create decorator
import { Reflector } from '@nestjs/core';
export const Roles = Reflector.createDecorator<string[]>();

// Usage
@Post()
@Roles(['admin'])
async create() {}

// Read in guard
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}
  canActivate(context: ExecutionContext): boolean {
    const roles = this.reflector.get(Roles, context.getHandler());
    if (!roles) return true;
    const { user } = context.switchToHttp().getRequest();
    return roles.some(r => user.roles?.includes(r));
  }
}
```

**Binding scope**: `@UseGuards(RolesGuard)` on class/method; `app.useGlobalGuards()` global; via `APP_GUARD` token for DI.

### 7. Interceptor — AOP Aspect

Implements `NestInterceptor`. Inserts logic before/after methods, can transform results/exceptions.

```ts
// Logging interceptor
@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(ctx: ExecutionContext, next: CallHandler): Observable<any> {
    const now = Date.now();
    return next.handle().pipe(
      tap(() => console.log(`After... ${Date.now() - now}ms`))
    );
  }
}

// Uniform response wrapper
@Injectable()
export class TransformInterceptor<T> implements NestInterceptor<T, {data: T}> {
  intercept(ctx: ExecutionContext, next: CallHandler) {
    return next.handle().pipe(map(data => ({ data })));
  }
}
```

### 8. Exception Filter

```ts
// Built-in exceptions
throw new BadRequestException('message');
throw new NotFoundException();
throw new UnauthorizedException();
// 20+ types: Forbidden, Conflict, InternalServerError, BadGateway, ...

// Custom
throw new HttpException('Forbidden', HttpStatus.FORBIDDEN);
throw new HttpException({ status: 403, error: 'custom' }, 403);
```

**Custom filter**:
```ts
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const res = ctx.getResponse<Response>();
    const status = exception.getStatus();
    res.status(status).json({ statusCode: status, timestamp: new Date().toISOString() });
  }
}
```

## Nest CLI

```bash
nest new <name>          # Create new project
nest g resource <name>   # Generate complete CRUD resource (module/controller/service/dto)
nest g module <name>     # Generate module
nest g controller <name> # Generate controller
nest g service <name>    # Generate service
nest g guard <name>      # Generate guard
nest g pipe <name>       # Generate pipe
nest g interceptor <name># Generate interceptor
nest g filter <name>     # Generate filter
nest build               # Compile
nest start               # Start
nest info                # System information
```

## OpenAPI (Swagger)

```bash
npm i @nestjs/swagger
```

```ts
// main.ts
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';

const config = new DocumentBuilder()
  .setTitle('API Docs').setVersion('1.0').addBearerAuth().build();

const documentFactory = () => SwaggerModule.createDocument(app, config);
SwaggerModule.setup('api', app, documentFactory);
// Access http://localhost:3000/api
```

Decorators: `@ApiTags()`, `@ApiOperation()`, `@ApiProperty()`, `@ApiResponse()`, `@ApiBearerAuth()`

## Common Technology Modules

### Database

Nest recommends using TypeORM (`@nestjs/typeorm`) or Prisma:

```bash
npm i @nestjs/typeorm typeorm pg
```

```ts
// app.module.ts
TypeOrmModule.forRoot({ type: 'postgres', host: 'localhost', database: 'mydb', autoLoadEntities: true, synchronize: true })

// feature module
TypeOrmModule.forFeature([User])
```

### Configuration Management

```bash
npm i @nestjs/config
```

```ts
// app.module.ts
ConfigModule.forRoot({ isGlobal: true, envFilePath: '.env' })

// Usage
constructor(private configService: ConfigService) {}
this.configService.get<string>('DATABASE_URL')
```

### Task Scheduling

```bash
npm i @nestjs/schedule
```
```ts
@Cron('45 * * * * *')  handleCron() {}
@Interval(10000)       handleInterval() {}
@Timeout(5000)         handleTimeout() {}
```

### Caching

```bash
npm i @nestjs/cache-manager cache-manager
```
`CacheModule.register()` + `@UseInterceptors(CacheInterceptor)`

## Global Registration vs DI Injection

Most Nest components support two global registration approaches:

```ts
// Method 1: Register directly in main.ts (cannot inject dependencies)
app.useGlobalPipes(new ValidationPipe());
app.useGlobalGuards(new RolesGuard());
app.useGlobalInterceptors(new LoggingInterceptor());
app.useGlobalFilters(new HttpExceptionFilter());

// Method 2: Register via Token in AppModule (supports DI)
providers: [
  { provide: APP_PIPE, useClass: ValidationPipe },
  { provide: APP_GUARD, useClass: RolesGuard },
  { provide: APP_INTERCEPTOR, useClass: LoggingInterceptor },
  { provide: APP_FILTER, useClass: HttpExceptionFilter },
]
```

## Request Lifecycle Order

```
1. Middleware
2. Guard
3. Interceptor (pre)
4. Pipe
5. Route Handler
6. Interceptor (post)
7. Exception Filter (if exception occurs)
```

## Recommended Directory Structure

```
src/
├── common/            # Shared: decorators, filters, guards, interceptors, pipes
├── config/            # Configuration
├── modules/
│   ├── users/
│   │   ├── dto/
│   │   ├── entities/
│   │   ├── users.controller.ts
│   │   ├── users.service.ts
│   │   └── users.module.ts
│   └── auth/
│       ├── dto/
│       ├── strategies/
│       ├── auth.controller.ts
│       ├── auth.service.ts
│       └── auth.module.ts
├── app.module.ts
└── main.ts
```

Detailed API reference see [references/api-reference.md](references/api-reference.md).