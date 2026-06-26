# Reglas JavaScript y TypeScript

Aplica a archivos con extensión: .js, .jsx, .ts, .tsx, .mjs, .cjs

---

## 🔴 BLOCKERS

### TypeScript Específico
- Uso de any sin justificación documentada en comentario
- Type assertions peligrosas: as any, as unknown as X
- @ts-ignore o @ts-nocheck sin comentario explicando por qué es necesario
- Interfaces vacías o con solo [key: string]: any
- Exportar tipos como any en APIs públicas del módulo
- Ignorar errores de TypeScript en lugar de corregirlos

❌ Mal:
  const data: any = fetchData();
  const user = response as any as User;
  // @ts-ignore
  const result = brokenFunction();

✅ Bien:
  interface ApiResponse {
    users: User[];
    total: number;
  }
  const data: ApiResponse = await fetchData();

### Async/Await
- Función marcada como async que nunca usa await
- await dentro de un loop cuando podría ser Promise.all()
- Funciones async sin manejo de errores
- Mezclar callbacks con async/await innecesariamente
- No retornar el resultado de una función async

❌ Mal (await secuencial innecesario):
  const results = [];
  for (const user of users) {
    const profile = await fetchProfile(user.id);
    results.push(profile);
  }

✅ Bien (paralelo cuando el orden no importa):
  const results = await Promise.all(
    users.map(user => fetchProfile(user.id))
  );

❌ Mal (async sin await):
  async function getName() {
    return 'John';
  }

✅ Bien (no necesita ser async):
  function getName() {
    return 'John';
  }

### React Específico (si aplica)
- useEffect sin array de dependencias causando loop infinito
- useEffect con dependencias incorrectas o faltantes
- Estado redundante que debería derivarse de otro estado
- Keys usando index en listas que pueden cambiar de orden
- setState dentro de useEffect sin condición de salida
- Llamadas a hooks dentro de condicionales o loops

❌ Mal:
  useEffect(() => {
    setCount(count + 1);
  }); // Sin dependencias = se ejecuta en cada render

  {items.map((item, index) => (
    <Item key={index} data={item} />
  ))}

✅ Bien:
  useEffect(() => {
    fetchData();
  }, []); // Se ejecuta solo una vez

  {items.map(item => (
    <Item key={item.id} data={item} />
  ))}

---

## 🟡 WARNINGS

### Comparaciones
- Usar == en lugar de === (comparación sin tipo)
- Usar != en lugar de !== (comparación sin tipo)
- Comparar con null usando == cuando debería ser === null o === undefined

❌ Mal:
  if (value == null) {}
  if (status == 1) {}

✅ Bien:
  if (value === null || value === undefined) {}
  if (value == null) {} // Solo este caso es aceptable como shorthand de null/undefined
  if (status === 1) {}

### Mutación de Estado
- Mutación directa de arrays: push, splice, sort en state de React
- Mutación directa de objetos de estado
- Modificar argumentos de funciones directamente

❌ Mal:
  state.items.push(newItem);
  state.user.name = 'John';

✅ Bien:
  setState(prev => ({ ...prev, items: [...prev.items, newItem] }));
  setState(prev => ({ ...prev, user: { ...prev.user, name: 'John' } }));

### Console Statements
- console.log que se quedó en código de producción
- console.error sin contexto útil
- console.warn innecesarios
- Excepción: console.error en catch blocks con información útil está permitido

### Timers sin Cleanup
- setTimeout sin clearTimeout en cleanup
- setInterval sin clearInterval en cleanup
- Especialmente importante en useEffect de React

❌ Mal:
  useEffect(() => {
    setInterval(() => {
      fetchData();
    }, 5000);
  }, []);

✅ Bien:
  useEffect(() => {
    const interval = setInterval(() => {
      fetchData();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

### Imports
- Imports no ordenados: agrupar por externos, internos, relativos
- Import de toda la librería cuando solo se usa una función
- Circular dependencies entre módulos

❌ Mal:
  import _ from 'lodash';
  const result = _.get(obj, 'path');

✅ Bien:
  import get from 'lodash/get';
  const result = get(obj, 'path');

### Tipado Débil (TypeScript)
- Parámetros sin tipo en funciones exportadas
- Return types implícitos en funciones públicas
- Union types excesivamente amplios
- Usar object o Function como tipo

---

## 🔵 SUGGESTIONS

### Modernización
- Preferir Array.includes() sobre múltiples ||
- Optional chaining ?. sobre verificaciones manuales de null
- Nullish coalescing ?? sobre || para valores por defecto
- Object.entries() y Object.values() sobre for...in
- Usar const sobre let siempre que sea posible, nunca var

❌ Antes:
  if (status === 'active' || status === 'pending' || status === 'review') {}
  if (user && user.address && user.address.city) {}
  const name = user.name || 'Anonymous'; // Bug: string vacío es falsy

✅ Después:
  if (['active', 'pending', 'review'].includes(status)) {}
  if (user?.address?.city) {}
  const name = user.name ?? 'Anonymous'; // Solo null/undefined

### Destructuring
- Usar destructuring cuando se accede a múltiples propiedades del mismo objeto
- Usar destructuring en parámetros de funciones para mayor claridad

❌ Antes:
  const name = props.user.name;
  const email = props.user.email;
  const age = props.user.age;

✅ Después:
  const { name, email, age } = props.user;

### Template Literals
- Preferir template literals sobre concatenación de strings

❌ Antes:
  const message = 'Hello ' + firstName + ' ' + lastName + ', welcome!';

✅ Después:
  const message = `Hello ${firstName} ${lastName}, welcome!`;

---

## 💡 NITS

### Estilo
- Preferir arrow functions para callbacks anónimos
- Preferir shorthand en objetos cuando la key y el value tienen el mismo nombre
- Usar trailing commas en objetos y arrays multilinea
- Consistencia en comillas: elegir simples o dobles y mantener en todo el proyecto

❌ Antes:
  const obj = { name: name, email: email };
  items.forEach(function(item) { return item.id; });

✅ Después:
  const obj = { name, email };
  items.forEach(item => item.id);