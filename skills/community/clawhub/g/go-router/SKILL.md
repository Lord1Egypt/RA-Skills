---
name: go-router
description: Declarative URL-based routing for Flutter using the Router API. Use when implementing navigation between screens, deep links, authentication guards, parameterized routes, shell routes with nested navigation, and web routing in Flutter apps.
---

# Go Router

GoRouter is a declarative routing package for Flutter that uses the Router API to provide convenient URL-based navigation.

## Core Concepts

### 1. Router Configuration

Define routes as a list of `GoRoute` objects:

```dart
final GoRouter _router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      path: '/user/:id',
      builder: (context, state) {
        final userId = state.pathParameters['id']!;
        return UserScreen(id: userId);
      },
    ),
  ],
);
```

### 2. Navigation

```dart
// Simple navigation
context.go('/details');

// With parameters
context.go('/user/123');

// Named navigation (requires name parameter)
context.goNamed('user', pathParameters: {'id': '123'});

// Push (adds to stack)
context.push('/modal');

// Replace current route
context.replace('/new');

// Go back
context.pop();

// With query parameters
context.go('/search?q=flutter');
```

### 3. Route Parameters

Path parameters use `:` prefix:

```dart
GoRoute(
  path: '/user/:id/posts/:postId',
  builder: (context, state) {
    final userId = state.pathParameters['id']!;
    final postId = state.pathParameters['postId']!;
    return PostScreen(userId: userId, postId: postId);
  },
)
```

Query parameters are accessed via `state.uri.queryParameters`:

```dart
GoRoute(
  path: '/search',
  builder: (context, state) {
    final query = state.uri.queryParameters['q'] ?? '';
    return SearchScreen(query: query);
  },
)
```

## Common Patterns

### Pattern 1: Authentication Guard with Redirection

```dart
final routerProvider = Provider<GoRouter>((ref) {
  final auth = ref.watch(authProvider);
  
  return GoRouter(
    initialLocation: '/',
    redirect: (context, state) {
      final isLoggedIn = auth.isLoggedIn;
      final isAuthRoute = state.matchedLocation == '/login';
      
      if (!isLoggedIn && !isAuthRoute) {
        return '/login';
      }
      if (isLoggedIn && isAuthRoute) {
        return '/';
      }
      return null;
    },
    routes: [
      GoRoute(path: '/login', builder: (_, __) => const LoginScreen()),
      GoRoute(path: '/', builder: (_, __) => const HomeScreen()),
    ],
  );
});
```

### Pattern 2: ShellRoute for Bottom Navigation

```dart
GoRouter(
  routes: [
    ShellRoute(
      builder: (context, state, child) {
        return ScaffoldWithNavBar(child: child);
      },
      routes: [
        GoRoute(
          path: '/',
          builder: (_, __) => const HomeScreen(),
        ),
        GoRoute(
          path: '/settings',
          builder: (_, __) => const SettingsScreen(),
        ),
      ],
    ),
  ],
)
```

### Pattern 3: StatefulShellRoute for Nested Navigation

```dart
StatefulShellRoute(
  branches: [
    StatefulShellBranch(
      routes: [GoRoute(path: '/feed', builder: (_, __) => FeedScreen())],
    ),
    StatefulShellBranch(
      routes: [GoRoute(path: '/profile', builder: (_, __) => ProfileScreen())],
    ),
  ],
)
```

### Pattern 4: Custom Page Transitions

```dart
GoRoute(
  path: '/details',
  pageBuilder: (context, state) => const MaterialPage(
    child: DetailsScreen(),
  ),
  // Or custom transition
  pageBuilder: (context, state) => CustomTransitionPage(
    child: const DetailsScreen(),
    transitionsBuilder: (context, animation, secondaryAnimation, child) {
      return FadeTransition(
        opacity: CurveTween(curve: Curves.easeInOut).animate(animation),
        child: child,
      );
    },
  ),
)
```

### Pattern 5: Error Handling

```dart
GoRouter(
  errorBuilder: (context, state) {
    return ErrorScreen(error: state.error);
  },
  // Or handle 404
  errorPageBuilder: (context, state) => MaterialPage(
    child: NotFoundScreen(path: state.uri.path),
  ),
)
```

### Pattern 6: Type-Safe Routes (Go Router 14+)

Define typed routes:

```dart
part 'app_routes.g.dart';

@TypedGoRoute<HomeRoute>(path: '/')
class HomeRoute extends GoRouteData {
  @override
  Widget build(BuildContext context, GoRouterState state) {
    return const HomeScreen();
  }
}

@TypedGoRoute<UserRoute>(path: '/user/:id')
class UserRoute extends GoRouteData {
  final String id;
  const UserRoute({required this.id});
  
  @override
  Widget build(BuildContext context, GoRouterState state) {
    return UserScreen(id: id);
  }
}
```

## Route State

Access route information in builders:

```dart
GoRoute(
  path: '/details',
  builder: (context, state) {
    // Path: state.uri.path
    // Query params: state.uri.queryParameters
    // Extra data: state.extra (passed via context.go('/details', extra: data))
    return DetailsScreen(
      path: state.uri.path,
      data: state.extra as MyData?,
    );
  },
)
```

## Navigation Helper Methods

```dart
// Extension for cleaner navigation
extension NavigationHelpers on BuildContext {
  void goHome() => go('/');
  void goUser(String id) => go('/user/$id');
  void pushModal(Widget screen) => push('/modal', extra: screen);
}

// Usage
context.goHome();
context.goUser('123');
```

## Web Support

Enable web URL handling:

```dart
GoRouter(
  // Handles browser back/forward
  // URL updates automatically
  initialLocation: '/',
  // For base href in web
  routerNeglect: true, // Disable browser history
)

// Access current route
final currentRoute = GoRouter.of(context).routeInformationProvider.value.uri.path;
```

## Route Observers

```dart
GoRouter(
  observers: [RouteObserver()],
  navigatorBuilder: (context, state, child) {
    // Wrap all routes
    return SomeWrapper(child: child);
  },
)
```

## Testing

```dart
testWidgets('navigates correctly', (tester) async {
  await tester.pumpWidget(
    MaterialApp.router(
      routerConfig: _router,
    ),
  );
  
  // Find and tap button
  await tester.tap(find.text('Go to details'));
  await tester.pumpAndSettle();
  
  // Verify navigation
  expect(find.text('Details'), findsOneWidget);
});
```

## Code Generation

For type-safe routes with code generation:

```bash
dart run build_runner build
```

Generates:
- `$route` constant for route location
- Parameter classes for typed routes

## Deep Linking

Configure Android & iOS for deep links, then handle in GoRouter:

```dart
GoRouter(
  routes: [
    GoRoute(
      path: '/product/:id',
      builder: (context, state) {
        // Handles myapp.com/product/123
        // and app://product/123
        return ProductScreen(id: state.pathParameters['id']!);
      },
    ),
  ],
)
```

## Navigation Without Context

```dart
// Store router reference
final GoRouter router = GoRouter(...);

// Navigate without context
router.go('/home');
router.push('/modal');
router.pop();
```

See [BEST_PRACTICES.md](BEST_PRACTICES.md) for architecture patterns.
