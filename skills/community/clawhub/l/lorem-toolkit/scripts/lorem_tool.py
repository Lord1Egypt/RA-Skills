#!/usr/bin/env python3
"""Lorem Toolkit - Placeholder text and fake data. Zero dependencies."""

import random
import string
import json
import sys
import argparse
from datetime import datetime, timedelta

LOREM_WORDS = [
    'lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit',
    'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore', 'et', 'dolore',
    'magna', 'aliqua', 'enim', 'ad', 'minim', 'veniam', 'quis', 'nostrud',
    'exercitation', 'ullamco', 'laboris', 'nisi', 'aliquip', 'ex', 'ea', 'commodo',
    'consequat', 'duis', 'aute', 'irure', 'in', 'reprehenderit', 'voluptate',
    'velit', 'esse', 'cillum', 'fugiat', 'nulla', 'pariatur', 'excepteur', 'sint',
    'occaecat', 'cupidatat', 'non', 'proident', 'sunt', 'culpa', 'qui', 'officia',
    'deserunt', 'mollit', 'anim', 'id', 'est', 'laborum', 'perspiciatis', 'unde',
    'omnis', 'iste', 'natus', 'error', 'voluptatem', 'accusantium', 'doloremque',
    'laudantium', 'totam', 'rem', 'aperiam', 'eaque', 'ipsa', 'quae', 'ab', 'illo',
    'inventore', 'veritatis', 'quasi', 'architecto', 'beatae', 'vitae', 'dicta',
    'explicabo', 'nemo', 'ipsam', 'quia', 'voluptas', 'aspernatur', 'aut', 'odit',
]

FIRST_NAMES_EN = ['James','Mary','Robert','Patricia','John','Jennifer','Michael','Linda','David','Elizabeth',
    'William','Barbara','Richard','Susan','Joseph','Jessica','Thomas','Sarah','Christopher','Karen']
LAST_NAMES_EN = ['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Rodriguez','Martinez',
    'Hernandez','Lopez','Gonzalez','Wilson','Anderson','Thomas','Taylor','Moore','Jackson','Martin']
FIRST_NAMES_CN = ['伟','芳','娜','敏','静','丽','强','磊','洋','艳','勇','军','杰','娟','涛','明','超','秀英','霞','平']
LAST_NAMES_CN = ['王','李','张','刘','陈','杨','赵','黄','周','吴','徐','孙','胡','朱','高','林','何','郭','马','罗']

CITIES_EN = ['New York','Los Angeles','Chicago','Houston','Phoenix','San Antonio','San Diego','Dallas','San Jose','Austin',
    'London','Paris','Berlin','Tokyo','Sydney','Toronto','Singapore','Hong Kong','Shanghai','Dubai']
CITIES_CN = ['北京','上海','广州','深圳','杭州','成都','武汉','南京','重庆','西安','苏州','天津','长沙','郑州','东莞']

DOMAINS = ['gmail.com','yahoo.com','outlook.com','hotmail.com','example.com','company.io','startup.co','mail.com']

def lorem_sentence():
    length = random.randint(8, 20)
    words = [random.choice(LOREM_WORDS) for _ in range(length)]
    words[0] = words[0].capitalize()
    return ' '.join(words) + '.'

def lorem_paragraph():
    sentences = random.randint(3, 7)
    return ' '.join(lorem_sentence() for _ in range(sentences))

def random_name(locale='en'):
    if locale == 'cn':
        return random.choice(LAST_NAMES_CN) + random.choice(FIRST_NAMES_CN)
    return random.choice(FIRST_NAMES_EN) + ' ' + random.choice(LAST_NAMES_EN)

def random_email(locale='en'):
    name = random_name(locale).lower().replace(' ', random.choice(['.', '_', '']))
    return f"{name}@{random.choice(DOMAINS)}"

def random_phone(locale='en'):
    if locale == 'cn':
        return '1' + str(random.choice([3,5,7,8,9])) + ''.join(str(random.randint(0,9)) for _ in range(9))
    return f"({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}"

def random_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

def random_mac():
    return ':'.join(f'{random.randint(0,255):02x}' for _ in range(6)).upper()

def random_url():
    domains = ['example','test','demo','sample','mysite','webapp']
    tlds = ['.com','.io','.co','.dev','.app','.org']
    return f"https://{random.choice(domains)}{random.choice(tlds)}/{random.choice(string.ascii_lowercase)}"

def random_date(year=None):
    year = year or random.randint(2020, 2026)
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31)
    delta = (end - start).days
    return (start + timedelta(days=random.randint(0, delta))).strftime('%Y-%m-%d')

def random_uuid():
    return ''.join(random.choices(string.hexdigits[:16], k=8)) + '-' + \
           ''.join(random.choices(string.hexdigits[:16], k=4)) + '-4' + \
           ''.join(random.choices(string.hexdigits[:16], k=3)) + '-' + \
           random.choice('89ab') + \
           ''.join(random.choices(string.hexdigits[:16], k=3)) + '-' + \
           ''.join(random.choices(string.hexdigits[:16], k=12))

def generate_pattern(pattern):
    result = []
    i = 0
    while i < len(pattern):
        if pattern[i] == '#':
            result.append(str(random.randint(0, 9)))
            i += 1
        elif pattern[i] == 'X':
            result.append(random.choice(string.ascii_uppercase))
            i += 1
        elif pattern[i] == 'x':
            result.append(random.choice(string.ascii_lowercase))
            i += 1
        elif pattern[i] == '*':
            result.append(random.choice(string.ascii_letters + string.digits))
            i += 1
        else:
            result.append(pattern[i])
            i += 1
    return ''.join(result)

def generate_users(count=5, locale='en'):
    users = []
    for _ in range(count):
        user = {
            'name': random_name(locale),
            'email': random_email(locale),
            'phone': random_phone(locale),
            'city': random.choice(CITIES_CN if locale == 'cn' else CITIES_EN),
            'age': random.randint(18, 70),
            'registered': random_date(),
        }
        users.append(user)
    return users

def main():
    parser = argparse.ArgumentParser(description='Lorem Toolkit')
    sub = parser.add_subparsers(dest='command')
    
    p = sub.add_parser('lorem', help='Lorem ipsum text')
    p.add_argument('-n', '--count', type=int, default=1)
    p.add_argument('-u', '--unit', choices=['paragraphs', 'sentences', 'words'], default='paragraphs')
    
    p = sub.add_parser('name', help='Random names')
    p.add_argument('-n', '--count', type=int, default=1)
    p.add_argument('-l', '--locale', choices=['en', 'cn'], default='en')
    
    p = sub.add_parser('email', help='Random emails')
    p.add_argument('-n', '--count', type=int, default=1)
    p.add_argument('-l', '--locale', choices=['en', 'cn'], default='en')
    
    p = sub.add_parser('phone', help='Random phones')
    p.add_argument('-n', '--count', type=int, default=1)
    p.add_argument('-l', '--locale', choices=['en', 'cn'], default='en')
    
    p = sub.add_parser('ip', help='Random IP addresses')
    p.add_argument('-n', '--count', type=int, default=1)
    
    p = sub.add_parser('date', help='Random dates')
    p.add_argument('-n', '--count', type=int, default=1)
    p.add_argument('-y', '--year', type=int)
    
    p = sub.add_parser('uuid', help='Random UUIDs')
    p.add_argument('-n', '--count', type=int, default=1)
    
    p = sub.add_parser('pattern', help='Generate from pattern (#=digit, X=upper, x=lower, *=alnum)')
    p.add_argument('pat'); p.add_argument('-n', '--count', type=int, default=1)
    
    p = sub.add_parser('users', help='Generate fake user JSON')
    p.add_argument('-n', '--count', type=int, default=5)
    p.add_argument('-l', '--locale', choices=['en', 'cn'], default='en')
    
    args = parser.parse_args()
    
    if args.command == 'lorem':
        if args.unit == 'paragraphs':
            for _ in range(args.count):
                print(lorem_paragraph() + '\n')
        elif args.unit == 'sentences':
            for _ in range(args.count):
                print(lorem_sentence())
        elif args.unit == 'words':
            print(' '.join(random.choice(LOREM_WORDS) for _ in range(args.count)))
    elif args.command == 'name':
        for _ in range(args.count):
            print(random_name(args.locale))
    elif args.command == 'email':
        for _ in range(args.count):
            print(random_email(args.locale))
    elif args.command == 'phone':
        for _ in range(args.count):
            print(random_phone(args.locale))
    elif args.command == 'ip':
        for _ in range(args.count):
            print(random_ip())
    elif args.command == 'date':
        for _ in range(args.count):
            print(random_date(args.year))
    elif args.command == 'uuid':
        for _ in range(args.count):
            print(random_uuid())
    elif args.command == 'pattern':
        for _ in range(args.count):
            print(generate_pattern(args.pat))
    elif args.command == 'users':
        print(json.dumps(generate_users(args.count, args.locale), ensure_ascii=False, indent=2))
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
