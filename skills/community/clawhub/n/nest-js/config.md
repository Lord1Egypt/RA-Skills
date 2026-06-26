# NestJS Configuration

## @nestjs/config (recommended)

### Basic Setup
```typescript
@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,          // available everywhere without importing
      envFilePath: ['.env.local', '.env'], // first found wins per variable
      ignoreEnvFile: process.env.NODE_ENV === 'production', // use real env vars in prod
    }),
  ],
})
export class AppModule {}
```

### Typed Configuration with Validation
```typescript
// config/database.config.ts
import { registerAs } from '@nestjs/config';

export default registerAs('database', () => ({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT, 10) || 5432,
  name: process.env.DB_NAME,
}));

// Usage with injection
@Injectable()
export class DbService {
  constructor(
    @Inject(databaseConfig.KEY)
    private dbConfig: ConfigType<typeof databaseConfig>,
  ) {
    // dbConfig.host, dbConfig.port — fully typed
  }
}
```

### Schema Validation with Joi
```typescript
import * as Joi from 'joi';

ConfigModule.forRoot({
  validationSchema: Joi.object({
    NODE_ENV: Joi.string().valid('development', 'production', 'test').default('development'),
    PORT: Joi.number().default(3000),
    DB_HOST: Joi.string().required(),
    DB_PORT: Joi.number().required(),
    JWT_SECRET: Joi.string().required(),
  }),
  validationOptions: {
    abortEarly: true, // fail fast on first error
  },
});
```

### Schema Validation with Zod (alternative)
```typescript
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.coerce.number().default(3000),
  DB_HOST: z.string(),
  JWT_SECRET: z.string().min(32),
});

ConfigModule.forRoot({
  validate: (config: Record<string, unknown>) => {
    const parsed = envSchema.safeParse(config);
    if (!parsed.success) {
      throw new Error(`Config validation error: ${parsed.error.message}`);
    }
    return parsed.data;
  },
});
```

## Common Traps

### `ConfigService.get()` Returns `undefined`
1. `ConfigModule` not imported in the module (or not `isGlobal: true`)
2. Env var not in `.env` file AND not in actual environment
3. Using `configService.get('database.host')` but didn't register namespaced config
4. `.env` file not in project root (relative to where `nest start` runs)

### Type Safety
```typescript
// ❌ Returns string | undefined — no type safety
const port = this.configService.get('PORT');

// ✅ Generic parameter
const port = this.configService.get<number>('PORT');

// ✅ With default (guarantees non-undefined)
const port = this.configService.get<number>('PORT', 3000);

// ✅ Best: use registerAs + ConfigType for full type safety
```

### Configuration at Bootstrap
```typescript
// main.ts — ConfigService isn't available before app is created
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  const configService = app.get(ConfigService);
  const port = configService.get<number>('PORT', 3000);
  await app.listen(port);
}
```

### Secrets Management
- Never commit `.env` with secrets — add to `.gitignore`
- Use `.env.example` with placeholder values for documentation
- In production, use real environment variables or a secrets manager (AWS SSM, Vault)
- `ConfigModule` with `ignoreEnvFile: true` in production — don't deploy .env files
- Validate required secrets at startup — fail fast, not on first request

### Async Configuration
```typescript
// When config depends on other async sources
TypeOrmModule.forRootAsync({
  imports: [ConfigModule],
  inject: [ConfigService],
  useFactory: (config: ConfigService) => ({
    type: 'postgres',
    host: config.get('DB_HOST'),
    port: config.get<number>('DB_PORT'),
    // ...
  }),
});
```
- `forRootAsync` with `useFactory` — when module config depends on ConfigService or other providers
- `inject` array specifies factory dependencies
- Always prefer `forRootAsync` over `forRoot` with `process.env` directly — ensures config is validated and centralized
