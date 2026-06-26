# NestJS Modules

## Core Concepts
- Every Nest app has a root `AppModule` — all other modules branch from it
- A module is a class decorated with `@Module()` containing `imports`, `controllers`, `providers`, `exports`
- Modules encapsulate providers — a provider is NOT available outside its module unless listed in `exports`

## Common Traps

### "Nest can't resolve dependencies of X"
This is the single most common NestJS error. Checklist:
1. Is the class decorated with `@Injectable()`?
2. Is it listed in the module's `providers` array?
3. If it's from another module, is that module listed in `imports`?
4. Does the source module `exports` the provider?
5. Are all of the provider's OWN dependencies also resolvable?

### Circular Module Dependencies
```typescript
// ❌ ModuleA imports ModuleB, ModuleB imports ModuleA — crash
// ✅ Use forwardRef on BOTH sides
@Module({
  imports: [forwardRef(() => ModuleB)],
})
export class ModuleA {}

@Module({
  imports: [forwardRef(() => ModuleA)],
})
export class ModuleB {}
```
Better fix: extract shared providers into a third module both can import.

### Global Modules
```typescript
@Global()
@Module({
  providers: [SharedService],
  exports: [SharedService],
})
export class SharedModule {}
```
- `@Global()` makes exports available everywhere WITHOUT importing the module
- Overuse defeats encapsulation — use sparingly (config, logging, database connections)

### Dynamic Modules
```typescript
@Module({})
export class DatabaseModule {
  static forRoot(options: DbOptions): DynamicModule {
    return {
      module: DatabaseModule,
      global: true, // optional
      providers: [
        { provide: 'DB_OPTIONS', useValue: options },
        DatabaseService,
      ],
      exports: [DatabaseService],
    };
  }

  static forFeature(entities: Type[]): DynamicModule {
    const providers = entities.map(entity => ({
      provide: getRepositoryToken(entity),
      useFactory: (ds: DataSource) => ds.getRepository(entity),
      inject: [DataSource],
    }));
    return {
      module: DatabaseModule,
      providers,
      exports: providers,
    };
  }
}
```
- `forRoot()` pattern: configure once in AppModule (connection, global config)
- `forFeature()` pattern: configure per-feature module (repositories, specific entities)
- `forRootAsync()`: when config depends on other providers (ConfigService)

### Module Re-exporting
```typescript
@Module({
  imports: [DatabaseModule],
  exports: [DatabaseModule], // re-export so importers get DatabaseModule's exports too
})
export class CoreModule {}
```

### Lazy-loaded Modules
```typescript
// For routes that should only load on demand (reduces startup time)
@Injectable()
export class SomeService {
  constructor(private lazyModuleLoader: LazyModuleLoader) {}

  async loadFeature() {
    const { FeatureModule } = await import('./feature.module');
    const moduleRef = await this.lazyModuleLoader.load(() => FeatureModule);
    const service = moduleRef.get(FeatureService);
  }
}
```
- Lazy modules don't register controllers/gateways — only providers
- Useful for serverless/cold-start optimization
