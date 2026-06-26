# NestJS Testing

## Unit Testing (Services)

```typescript
describe('UsersService', () => {
  let service: UsersService;
  let repo: jest.Mocked<Repository<User>>;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        UsersService,
        {
          provide: getRepositoryToken(User),
          useValue: {
            find: jest.fn(),
            findOne: jest.fn(),
            save: jest.fn(),
            delete: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get(UsersService);
    repo = module.get(getRepositoryToken(User));
  });

  it('should find all users', async () => {
    const users = [{ id: 1, name: 'Alice' }] as User[];
    repo.find.mockResolvedValue(users);
    expect(await service.findAll()).toEqual(users);
  });
});
```

## Unit Testing (Controllers)

```typescript
describe('UsersController', () => {
  let controller: UsersController;
  let service: jest.Mocked<UsersService>;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      controllers: [UsersController],
      providers: [
        {
          provide: UsersService,
          useValue: {
            findAll: jest.fn(),
            create: jest.fn(),
          },
        },
      ],
    }).compile();

    controller = module.get(UsersController);
    service = module.get(UsersService);
  });
});
```

## Integration / E2E Testing

```typescript
describe('Users (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture = await Test.createTestingModule({
      imports: [AppModule],
    })
      .overrideProvider(DatabaseService)
      .useValue(mockDatabaseService) // swap real DB for mock
      .compile();

    app = moduleFixture.createNestApplication();
    // ⚠️ Apply same global pipes/guards/interceptors as main.ts
    app.useGlobalPipes(new ValidationPipe({ whitelist: true }));
    await app.init();
  });

  afterAll(async () => {
    await app.close(); // ⚠️ prevents hanging tests and connection leaks
  });

  it('/users (GET)', () => {
    return request(app.getHttpServer())
      .get('/users')
      .expect(200)
      .expect(res => {
        expect(res.body).toBeInstanceOf(Array);
      });
  });

  it('/users (POST) validates body', () => {
    return request(app.getHttpServer())
      .post('/users')
      .send({ name: '' }) // invalid
      .expect(400);
  });
});
```

## Common Traps

### E2E Tests Don't Apply Global Config
```typescript
// ❌ Global pipes/guards set in main.ts are NOT applied in Test.createTestingModule
// Your e2e tests will pass without validation, giving false confidence

// ✅ Apply the same global config in test setup
app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
app.useGlobalFilters(new AllExceptionsFilter());
```

### `Test.createTestingModule` Creates Full DI Container
- All providers must be resolvable — either real or mocked
- Use `.overrideProvider(Token).useValue(mock)` to swap implementations
- For large module graphs, import only the module under test + mock its imports

### Mocking the Repository
```typescript
// ❌ Providing Repository class directly — Nest tries to connect to DB
providers: [UsersService, Repository],

// ✅ Mock the specific repository token
{ provide: getRepositoryToken(User), useValue: mockRepo }
```

### Testing Guards
```typescript
// Override guard globally for e2e tests that shouldn't auth
const module = await Test.createTestingModule({ imports: [AppModule] })
  .overrideGuard(AuthGuard)
  .useValue({ canActivate: () => true })
  .compile();
```

### Testing with Real Database
```typescript
// Use a test database container (testcontainers)
import { PostgreSqlContainer } from '@testcontainers/postgresql';

let container: StartedPostgreSqlContainer;

beforeAll(async () => {
  container = await new PostgreSqlContainer().start();
  // Use container.getConnectionUri() for TypeORM/Prisma config
}, 30000); // containers take time to start

afterAll(async () => {
  await container.stop();
});
```

### Hanging Tests
- `afterAll(() => app.close())` — always close the app to release connections
- Database connections not closed — especially with TypeORM/Prisma
- Open handles from event emitters, intervals, or WebSocket connections
- Use `--forceExit` as last resort, but fix the underlying leak

### Request-Scoped Providers in Tests
```typescript
// Request-scoped providers can't be resolved with module.get()
// ✅ Use module.resolve() instead
const service = await module.resolve(RequestScopedService);
```

### Custom Test Utilities
```typescript
// Create a reusable test module factory
export async function createTestApp(overrides?: {
  providers?: Provider[];
}) {
  const builder = Test.createTestingModule({ imports: [AppModule] });

  overrides?.providers?.forEach(p => {
    builder.overrideProvider(p.provide).useValue(p.useValue);
  });

  const module = await builder.compile();
  const app = module.createNestApplication();
  app.useGlobalPipes(new ValidationPipe({ whitelist: true }));
  await app.init();
  return app;
}
```
