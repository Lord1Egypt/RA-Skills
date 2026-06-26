# Go Router Best Practices

## Architecture

### Centralize Route Definitions

Keep all routes in one file:

```dart
// routing/routes.dart
class Routes {
  static const String home = '/';
  static const String user = '/user/:id';
  static const String settings = '/settings';
}

// routing/app_router.dart
final routerProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    routes: [
      GoRoute(path: Routes.home, builder: (_, __) => const HomeScreen()),
      GoRoute(path: Routes.user, builder: (_, state) => UserScreen(id: state.pathParameters['id']!)),
      GoRoute(path: Routes.settings, builder: (_, __) => const SettingsScreen()),
    ],
  );
});
```

### Route Guards Pattern

```dart
GoRouter(
  routes: [
    GoRoute(
      path: '/admin',
      builder: (context, state) {
        final user = ref.watch(userProvider);
        if (!user.isAdmin) {
          return const AccessDeniedScreen();
        }
        return const AdminScreen();
      },
    ),
  ],
)
```

## Deep Links

Configure for both mobile and web:

```dart
// Handle app://product/123
// and https://example.com/product/123
GoRoute(
  path: '/product/:id',
  builder: (context, state) {
    final id = state.pathParameters['id']!;
    return ProductScreen(id: id);
  },
)
```

## Common Anti-Patterns

### ❌ Don't: Use context after navigation

```dart
// BAD - context may be unmounted
context.go('/new');
ScaffoldMessenger.of(context).showSnackBar(...);
```

### ✅ Do: Navigate then show snackbar

```dart
// Show snackbar before navigation
ScaffoldMessenger.of(context).showSnackBar(...);
context.go('/new');

// Or use GoRouter's observer
```

### ❌ Don't: Call go/pop in initState

```dart
// BAD
@override
void initState() {
  context.go('/other'); // No context in initState
}
```

### ✅ Do: Use WidgetsBinding or postFrame

```dart
@override
void initState() {
  super.initState();
  WidgetsBinding.instance.addPostFrameCallback((_) {
    context.go('/other');
  });
}
```

## Performance

### Avoid Rebuilding Router

Use `Provider` for router, not `StateProvider`:

```dart
// GOOD - Router doesn't rebuild on auth changes
final routerProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    redirect: (context, state) {
      // This runs on every navigation
      final auth = ref.read(authProvider);
      if (!auth.isLoggedIn) return '/login';
      return null;
    },
  );
});
```

### Lazy Load Screens

```dart
GoRoute(
  path: '/heavy',
  builder: (context, state) {
    return const HeavyScreen(); // Lazy loaded
  },
  // Or use deferred imports
)
```

## Testing

```dart
void testNavigation() {
  final router = GoRouter(routes: ...);
  
  router.go('/user/123');
  expect(router.routeInformationProvider.value.uri.path, '/user/123');
}
```
