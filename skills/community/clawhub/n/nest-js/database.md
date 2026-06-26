# NestJS Database Integration

## TypeORM

### Setup
```typescript
// app.module.ts
@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: process.env.DB_HOST,
      port: parseInt(process.env.DB_PORT, 10),
      entities: [__dirname + '/**/*.entity{.ts,.js}'],
      // OR use autoLoadEntities: true (recommended with forFeature)
      synchronize: false, // ⚠️ NEVER true in production
    }),
  ],
})

// feature module
@Module({
  imports: [TypeOrmModule.forFeature([User, Profile])],
  providers: [UsersService],
})
export class UsersModule {}
```

### Repository Pattern
```typescript
@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private usersRepo: Repository<User>,
  ) {}

  findAll(): Promise<User[]> {
    return this.usersRepo.find({ relations: ['profile'] });
  }
}
```

### Common TypeORM + Nest Traps
- `synchronize: true` in production — drops/recreates tables, DATA LOSS. Use migrations.
- Entity not in `entities` array AND `autoLoadEntities` is false — "No metadata found" error
- `autoLoadEntities` only finds entities registered via `forFeature()` — manual entity classes not in any forFeature are missed
- Circular entity relations — `@ManyToOne(() => User)` lazy-callback syntax required
- Transaction handling — use `DataSource.transaction()` or `QueryRunner`, not multiple separate repo saves
- Repository injected but module doesn't import `TypeOrmModule.forFeature([Entity])` — "can't resolve Repository" error

### Migrations
```bash
# Generate migration from entity changes
npx typeorm migration:generate -d src/data-source.ts src/migrations/AddUserTable
# Run migrations
npx typeorm migration:run -d src/data-source.ts
```
- Separate `data-source.ts` for CLI — can't use Nest DI in migration CLI
- Always review generated migrations before running

## Prisma

### Setup
```typescript
// prisma.service.ts
@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit {
  async onModuleInit() {
    await this.$connect();
  }

  async onModuleDestroy() {
    await this.$disconnect();
  }
}

// prisma.module.ts
@Global()
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
```

### Usage
```typescript
@Injectable()
export class UsersService {
  constructor(private prisma: PrismaService) {}

  findAll() {
    return this.prisma.user.findMany({ include: { posts: true } });
  }

  create(data: CreateUserDto) {
    return this.prisma.user.create({ data });
  }
}
```

### Common Prisma + Nest Traps
- Not calling `$connect()` in `onModuleInit` — first query is slow (lazy connect)
- Not calling `$disconnect()` in `onModuleDestroy` — connection pool leaks in tests and serverless
- Prisma generates its own types — don't duplicate with DTOs for database layer, use Prisma types directly for repository logic; DTOs for API boundary
- `enableShutdownHooks` conflicts with Nest's own shutdown — use `onModuleDestroy` instead of Prisma's built-in shutdown hook

## Mongoose

### Setup
```typescript
@Module({
  imports: [
    MongooseModule.forRoot('mongodb://localhost/nest'),
    MongooseModule.forFeature([{ name: Cat.name, schema: CatSchema }]),
  ],
})

// Schema definition
@Schema({ timestamps: true })
export class Cat {
  @Prop({ required: true })
  name: string;

  @Prop({ type: mongoose.Schema.Types.ObjectId, ref: 'Owner' })
  owner: Owner;
}

export const CatSchema = SchemaFactory.createForClass(Cat);
```

### Common Mongoose + Nest Traps
- `@Prop()` without `required: true` — field is optional by default, unlike class-validator
- Schema definition separate from validation — Mongoose schema validates at DB level, class-validator at API level; you need both
- `@InjectModel(Cat.name)` — must match the name in `forFeature()` registration exactly
- Virtual properties need `toJSON: { virtuals: true }` in schema options
- Discriminators for inheritance — use `MongooseModule.forFeature` with `discriminators` option

## General Database Traps in NestJS
- Transactions across services — inject `DataSource`/`EntityManager` and pass transaction manager, don't rely on separate repository calls
- Connection not closed on app shutdown — enable `enableShutdownHooks()` in main.ts
- N+1 queries — use `relations` (TypeORM), `include` (Prisma), or `.populate()` (Mongoose) to eager-load
- Connection pool exhaustion — default pools are small (10), increase for production
