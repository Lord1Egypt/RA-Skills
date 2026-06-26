# NestJS Microservices, Queues & WebSockets

## Microservices (Transport Layer)

### Setup
```typescript
// main.ts — hybrid app (HTTP + microservice)
const app = await NestFactory.create(AppModule);
app.connectMicroservice<MicroserviceOptions>({
  transport: Transport.TCP,
  options: { host: '0.0.0.0', port: 3001 },
});
await app.startAllMicroservices();
await app.listen(3000);
```

### Message Patterns (Request/Response)
```typescript
// Service (listener)
@Controller()
export class MathController {
  @MessagePattern({ cmd: 'sum' })
  sum(data: number[]): number {
    return data.reduce((a, b) => a + b, 0);
  }
}

// Client (caller)
@Injectable()
export class AppService {
  constructor(@Inject('MATH_SERVICE') private client: ClientProxy) {}

  getSum(numbers: number[]) {
    return this.client.send({ cmd: 'sum' }, numbers); // returns Observable
  }
}

// Register client
@Module({
  imports: [
    ClientsModule.register([{
      name: 'MATH_SERVICE',
      transport: Transport.TCP,
      options: { host: 'math-service', port: 3001 },
    }]),
  ],
})
```

### Event Patterns (Fire-and-Forget)
```typescript
// Listener
@EventPattern('user.created')
handleUserCreated(data: UserCreatedEvent) {
  // no return value — fire and forget
}

// Emitter
this.client.emit('user.created', { userId: 1, email: 'a@b.com' });
```

### Transport Options
- `Transport.TCP` — default, simple, no broker needed
- `Transport.REDIS` — Redis pub/sub
- `Transport.NATS` — NATS messaging
- `Transport.MQTT` — IoT/lightweight
- `Transport.KAFKA` — high-throughput event streaming
- `Transport.RMQ` — RabbitMQ
- `Transport.GRPC` — Protocol Buffers, strongly typed

### Common Microservice Traps
- `client.send()` returns cold Observable — must `.subscribe()` or convert to Promise with `firstValueFrom()`
- Forgetting `await app.startAllMicroservices()` — microservice transport never starts
- `ClientProxy` not connected — call `client.connect()` or it auto-connects on first message (but first message is slow)
- Serialization — objects must be JSON-serializable across transport; classes become plain objects
- Error propagation — exceptions in microservice handler propagate to caller as `RpcException`, not `HttpException`

## Bull Queues (@nestjs/bull or @nestjs/bullmq)

### Setup
```typescript
@Module({
  imports: [
    BullModule.forRoot({ connection: { host: 'localhost', port: 6379 } }),
    BullModule.registerQueue({ name: 'email' }),
  ],
  providers: [EmailProcessor],
})

// Producer
@Injectable()
export class EmailService {
  constructor(@InjectQueue('email') private emailQueue: Queue) {}

  async sendWelcome(userId: string) {
    await this.emailQueue.add('welcome', { userId }, {
      delay: 5000,           // delay 5 seconds
      attempts: 3,           // retry up to 3 times
      backoff: { type: 'exponential', delay: 1000 },
      removeOnComplete: true,
    });
  }
}

// Consumer
@Processor('email')
export class EmailProcessor {
  @Process('welcome')
  async handleWelcome(job: Job<{ userId: string }>) {
    // process the job
    // throw to retry, return to complete
  }

  @OnQueueFailed()
  onFailed(job: Job, error: Error) {
    console.error(`Job ${job.id} failed:`, error.message);
  }
}
```

### Queue Traps
- Queue name mismatch between `registerQueue` and `@Processor` — silently never processes
- Redis not running — queue operations hang or throw, no clear error
- Job data not serializable — functions, circular refs, class instances fail
- Processor not in module's providers — Nest doesn't discover it

## WebSockets (@nestjs/websockets)

### Gateway
```typescript
@WebSocketGateway({
  cors: { origin: '*' },
  namespace: '/chat',
})
export class ChatGateway implements OnGatewayConnection, OnGatewayDisconnect {
  @WebSocketServer()
  server: Server;

  handleConnection(client: Socket) {
    console.log(`Connected: ${client.id}`);
  }

  handleDisconnect(client: Socket) {
    console.log(`Disconnected: ${client.id}`);
  }

  @SubscribeMessage('message')
  handleMessage(client: Socket, payload: { room: string; text: string }) {
    this.server.to(payload.room).emit('message', payload);
    return { event: 'message', data: 'received' }; // ack to sender
  }
}
```

### WebSocket Traps
- Guards/pipes/interceptors work with gateways — but use `context.switchToWs()` not `switchToHttp()`
- CORS not configured on gateway — browser connections fail silently
- `@WebSocketServer()` is undefined in constructor — only available after `onModuleInit`
- Namespace mismatch — client connects to `/chat` but gateway is on `/` or vice versa
- Authentication — middleware doesn't run for WS; use a guard or handle in `handleConnection`

## Server-Sent Events (SSE)
```typescript
@Sse('events')
sse(): Observable<MessageEvent> {
  return interval(1000).pipe(
    map(n => ({ data: { count: n } } as MessageEvent)),
  );
}
```
- Returns Observable that streams events to client
- Connection stays open — be mindful of resource usage
- Client uses `EventSource` API
