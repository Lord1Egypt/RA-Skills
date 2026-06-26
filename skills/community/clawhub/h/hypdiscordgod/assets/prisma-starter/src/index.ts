import 'dotenv/config';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  const guilds = await prisma.guildSettings.findMany({ take: 10 });
  console.log(guilds);
}

main().finally(() => prisma.$disconnect());
