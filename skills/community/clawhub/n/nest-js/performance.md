# NestJS Performance

## Caching

### Built-in Cache Manager
```typescript
// app.module.ts
import { CacheModule } from '@nestjs/cache-manager';

@Module({
  imports: [
    CacheModule.register({
      ttl: 60, // seconds (v5+) or milliseconds (v4)
      max: 100, // max items in cache
      isGlobal: true,
    }),
  ],
})

// With Redis store
import { redisStore } from 'cache-manager-redis-store';
CacheModule.registerAsync({
  useFactory: async () => ({
    store: await redisStore({ host: 'localhost', port: 6379 }),
    ttl: 60,
  }),
});
```

### Cache Interceptor (auto-cache GET routes)
```typescript
@UseInterceptors(CacheInterceptor)
@Controller('products')
export class ProductsController {
  @CacheTTL(120) // override default TTL for this route
  @CacheKey('all-products') // custom cache key
  @Get()
  findAll() { return this.productsService.findAll(); }
}
```

### Manual Cache Usage
```typescript
@Injectable()
export class UsersService {
  constructor(@Inject(CACHE_MANAGER) private cache: Cache) {}

  async findOne(id: number) {
    const cached = await this.cache.get<User>(`user:${id}`);
    if (cached) return cached;
    const user = await this.repo.findOne({ where: { id } });
    await this.cache.set(`user:${id}`, user, 300);
    return user;
  }
}
```

### Cache Traps
- `CacheInterceptor` only caches GET — POST/PUT/DELETE are ignored
- Cache key includes query params by default — `?page=1` and `?page=2` are separate
- Stale cache after mutations — manually `cache.del()` after writes
- Redis serialization — class instances become plain objects when deserialized
- `CacheModule` v4 vs v5 — TTL units changed from ms to seconds

## Fastify Adapter

```typescript
// main.ts
import { NestFactory } from '@nestjs/core';
import { FastifyAdapter, NestFastifyApplication } from '@nestjs/platform-fastify';

const app = await NestFactory.create<NestFastifyApplication>(
  AppModule,
  new FastifyAdapter(),
);
await app.listen(3000, '0.0.0.0'); // ⚠️ Fastify binds 127.0.0.1 by default
```

### Fastify Traps
- Listen on `'0.0.0.0'` not default — Docker/containers can't reach `127.0.0.1`
- Express middleware (multer, passport) won't work — use Fastify equivalents
- `@Req()` and `@Res()` types change — `FastifyRequest`/`FastifyReply` not Express types
- Multer → `@fastify/multipart`, Helmet → `@fastify/helmet`, etc.
- ~2x throughput over Express for JSON APIs

## Serialization & Response Performance

### ClassSerializerInterceptor
```typescript
// Exclude sensitive fields globally
@UseInterceptors(ClassSerializerInterceptor)
@Controller()
export class AppController {}

// In entity/DTO
@Exclude()
password: string;

@Expose({ groups: ['admin'] })
internalNotes: string;

// Serialize with groups
@SerializeOptions({ groups: ['admin'] })
@Get('admin/users')
findAllAdmin() {}
```

### Custom Serialization
```typescript
// For complex transformation, a dedicated interceptor is cleaner
@Injectable()
export class TransformInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler) {
    return next.handle().pipe(
      map(data => ({
        success: true,
        data,
        timestamp: Date.now(),
      })),
    );
  }
}
```

## Compression & Helmet
```typescript
import compression from 'compression';
import helmet from 'helmet';

app.use(compression());
app.use(helmet());
// Fastify: app.register(fastifyCompress); app.register(fastifyHelmet);
```

## Streaming Large Responses
```typescript
@Get('export')
export(@Res({ passthrough: true }) res: Response) {
  const stream = this.service.getDataStream();
  res.set({ 'Content-Type': 'text/csv' });
  return new StreamableFile(stream);
}
```
- `StreamableFile` — Nest-native way to stream, works with both Express and Fastify
- Don't buffer large datasets in memory — stream from database/file

## Shutdown Hooks
```typescript
// main.ts
app.enableShutdownHooks();

// In a service
@Injectable()
export class CleanupService implements OnModuleDestroy {
  async onModuleDestroy() {
    // Close connections, flush buffers, drain queues
    await this.db.disconnect();
    await this.cache.quit();
  }
}
```
- Without `enableShutdownHooks()`, `onModuleDestroy` / `beforeApplicationShutdown` never fire
- Crucial for graceful shutdown in Kubernetes / containerized deployments
- Handles SIGTERM, SIGINT

## Lazy Loading Modules
```typescript
// Reduces startup time by loading modules on demand
const { HeavyModule } = await import('./heavy.module');
const moduleRef = await this.lazyModuleLoader.load(() => HeavyModule);
```
- Serverless / cold-start optimization
- Lazy modules can't register controllers — only providers
