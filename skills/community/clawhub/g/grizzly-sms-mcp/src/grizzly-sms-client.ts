import axios, { AxiosInstance } from 'axios';

export interface ActivationRequest {
  service: string;
  country?: number | string; // Can be number, "*", or "any"
  operator?: string;
  forward?: number;
  ref?: string;
  maxPrice?: number;
  providerIds?: string;
  exceptProviderIds?: string;
  phoneException?: string;
  activationType?: number;
  ref_id?: string;
}

export interface Activation {
  id: string;
  phone: string;
  activationId: string;
  service: string;
  status: string;
  code?: string;
  createdAt: string;
}

export interface Balance {
  balance: number;
  currency: string;
}

export interface ServicePrice {
  service: string;
  country: number;
  price: number;
  count: number;
}

export class GrizzlySMSClient {
  private client: AxiosInstance;
  private apiKey: string;

  constructor(apiKey: string, baseURL: string = 'https://api.grizzlysms.com') {
    this.apiKey = apiKey;
    this.client = axios.create({
      baseURL,
      timeout: 30000,
    });
  }

  private async makeRequest(params: Record<string, any>): Promise<any> {
    try {
      const response = await this.client.get('/stubs/handler_api.php', {
        params: {
          api_key: this.apiKey,
          ...params,
        },
        transformResponse: [(data: any, headers: any) => {
          const contentType = headers['content-type'] || '';
          if (contentType.includes('application/json')) {
            try {
              return JSON.parse(data);
            } catch {
              return data;
            }
          }
          return data;
        }],
      });
      
      const data = response.data;
      
      if (typeof data === 'string') {
        if (data === 'NO_KEY' || data.startsWith('NO_KEY')) {
          throw new Error('NO_KEY - Invalid or missing API key');
        }
        if (data === 'SERVICE_UNAVAILABLE_REGION') {
          throw new Error('SERVICE_UNAVAILABLE_REGION - Access from your region is forbidden');
        }
        if (data === 'USERS_IP_IS_NOT_ALLOWED') {
          throw new Error('USERS_IP_IS_NOT_ALLOWED - IP address not allowed');
        }
        
        if (data.startsWith('BAD_') || data.startsWith('NO_') || data.startsWith('ERROR_') || data.startsWith('WRONG_')) {
          throw new Error(data);
        }
        
        return data;
      }
      
      return data;
    } catch (error: any) {
      if (error.message && error.message.startsWith('NO_KEY') || 
          error.message.startsWith('SERVICE_UNAVAILABLE_REGION') ||
          error.message.startsWith('USERS_IP_IS_NOT_ALLOWED') ||
          error.message.startsWith('BAD_') ||
          error.message.startsWith('NO_') ||
          error.message.startsWith('ERROR_') ||
          error.message.startsWith('WRONG_')) {
        throw error;
      }
      
      if (error.response) {
        const errorData = error.response.data;
        if (typeof errorData === 'string') {
          throw new Error(errorData);
        }
        throw new Error(`API Error: ${JSON.stringify(errorData)}`);
      }
      if (error.message) {
        throw error;
      }
      throw new Error(`Request failed: ${error.message || 'Unknown error'}`);
    }
  }

  async getBalance(includeReserve: boolean = false): Promise<Balance> {
    const params: any = { action: 'getBalance' };
    if (includeReserve) {
      params.version = '2';
    }
    
    const response = await this.makeRequest(params);
    
    if (typeof response === 'string') {
      const parts = response.split(':');
      if (parts[0] === 'ACCESS_BALANCE') {
        return {
          balance: parseFloat(parts[1]),
          currency: 'USD',
        };
      }
    }
    
    throw new Error('Invalid balance response');
  }

  async getNumber(request: ActivationRequest, version: 'v1' | 'v2' = 'v1'): Promise<{ activationId: string; phone: string; [key: string]: any }> {
    let action = 'getNumber';
    if (version === 'v2') {
      action = 'getNumberV2';
    }
    
    const params: any = {
      action,
      service: request.service,
    };
    
    if (request.country !== undefined) {
      if (request.country === '*' || request.country === 'any') {
        params.country = '*';
      } else {
        params.country = request.country;
      }
    }
    
    if (request.operator) params.operator = request.operator;
    if (request.forward !== undefined) params.forward = request.forward;
    if (request.ref) params.ref = request.ref;
    if (request.ref_id) params.ref_id = request.ref_id;
    if (request.maxPrice !== undefined) params.maxPrice = request.maxPrice;
    if (request.providerIds) params.providerIds = request.providerIds;
    if (request.exceptProviderIds) params.exceptProviderIds = request.exceptProviderIds;
    if (request.phoneException) params.phoneException = request.phoneException;
    if (request.activationType !== undefined) params.activationType = request.activationType;
    
    const response = await this.makeRequest(params);
    
    // Handle V1 response: ACCESS_NUMBER:{activation_id}:{phone_number}
    if (typeof response === 'string' && response.startsWith('ACCESS_NUMBER')) {
      const parts = response.split(':');
      return {
        activationId: parts[1],
        phone: parts[2],
      };
    }
    
    // Handle V2 response: JSON with activationId, phoneNumber...
    if (version === 'v2' && typeof response === 'object') {
      return {
        activationId: String(response.activationId || response.act_id),
        phone: response.phoneNumber || response.number || response.phone,
        activationCost: response.activationCost,
        currency: response.currency,
        countryCode: response.countryCode,
        canGetAnotherSms: response.canGetAnotherSms,
        activationTime: response.activationTime,
      };
    }
    
    if (typeof response === 'object') {
      return {
        activationId: String(response.activationId || response.act_id || response.id || ''),
        phone: response.phoneNumber || response.number || response.phone || '',
        ...response,
      };
    }
    
    throw new Error('Invalid response format from getNumber');
  }

  async setStatus(activationId: string, status: number): Promise<{ status: string }> {
    const response = await this.makeRequest({
      action: 'setStatus',
      id: activationId,
      status,
    });
    
    if (typeof response === 'string') {
      if (response === 'ACCESS_READY') {
        return { status: 'READY' };
      }
      if (response === 'ACCESS_RETRY_GET') {
        return { status: 'RETRY_GET' };
      }
      if (response === 'ACCESS_ACTIVATION') {
        return { status: 'ACTIVATION' };
      }
      if (response === 'ACCESS_CANCEL') {
        return { status: 'CANCEL' };
      }
      return { status: response };
    }
    
    return response;
  }

  async getStatus(activationId: string): Promise<{ status: string; code?: string }> {
    const response = await this.makeRequest({
      action: 'getStatus',
      id: activationId,
    });
    
    if (typeof response === 'string') {
      if (response === 'STATUS_WAIT_CODE' || response.startsWith('STATUS_WAIT_CODE')) {
        return { status: 'WAIT_CODE' };
      }
      
      if (response.startsWith('STATUS_WAIT_RETRY')) {
        const parts = response.split(':');
        return { status: 'WAIT_RETRY', code: parts[1] };
      }
      
      if (response === 'STATUS_WAIT_RESEND' || response.startsWith('STATUS_WAIT_RESEND')) {
        return { status: 'WAIT_RESEND' };
      }
      
      if (response.startsWith('STATUS_OK')) {
        const parts = response.split(':');
        return { status: 'OK', code: parts[1] };
      }
      
      if (response === 'STATUS_CANCEL' || response.startsWith('STATUS_CANCEL')) {
        return { status: 'CANCEL' };
      }
    }
    
    return response;
  }

  async getPrices(country?: number | string, service?: string, version: 'v1' | 'v2' | 'v3' = 'v1'): Promise<any> {
    let action = 'getPrices';
    if (version === 'v2') {
      action = 'getPricesV2';
    } else if (version === 'v3') {
      action = 'getPricesV3';
    }
    
    const params: any = { action };
    
    if (country !== undefined) {
      if (country === '*' || country === 'any') {
        params.country = '*';
      } else {
        params.country = country;
      }
    }
    
    if (service) params.service = service;
    
    return await this.makeRequest(params);
  }

  async getCountries(): Promise<any> {
    return await this.makeRequest({ action: 'getCountries' });
  }

  async getServices(): Promise<any> {
    return await this.makeRequest({ action: 'getServicesList' });
  }

  async getWallet(coin: string = 'usdt', network: string = 'tron'): Promise<{ wallet_address: string }> {
    const response = await this.client.get('/public/crypto/wallet', {
      params: {
        api_key: this.apiKey,
        coin,
        network,
      },
    });
    return response.data;
  }
}

