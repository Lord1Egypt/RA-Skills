const EMPTY_CUST={dlg:false,name:'',address:'',contact:'',cmt:''}
const BATCH_NUM=150;
export default {
inject:['service', 'tags', "icons"],
data() {return {
    customers:[], //客户列表
    customer:{},
    search:'',
    percent:{val:0,each:0},
    page:{cur:1, max:0},
    tmpls:[],
    tmpl:'',
    custInfo:cloneObj(EMPTY_CUST),
    shipInfo:{dlg:false,codes:[],customer:0,sellAt:'',name:''}
}},
created(){
    this.service.getCustDtl().then(cust=> {
        this.customer = cust;
        if(cust.id==0) {
            this.query_custs(1);
        }
    });
    this.service.getTmpls(true).then(tmpls=>{
        var opts=[];
        for(var t of tmpls) {
            opts.push({label:t.name,value:t.tpl});
        }
        this.tmpls=opts;
    })
},
methods:{
fmt_customer_lines(data) {
    var dt=new Date();
    var customers=[];
    var cols=data.cols;
    var cu;
    for(var row of data.customers) {
        cu={};
        for(var i in cols) {
            cu[cols[i]]=row[i];
        }
        dt.setTime(cu.createAt*60000);
        cu.createAt=date2str(dt);
        customers.push(cu);
    }
    this.customers=customers;
},
query_custs(pg) {
    this.search='';
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var url = "/api/customer/list?offset="+offset+"&num="+this.service.N_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK || resp.data.total==0) {
            this.customers=[];
            this.page.max=0;
            this.page.cur=1;
            return;
        }
        this.fmt_customer_lines(resp.data);
        this.page.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
search_custs() {
    if(this.search=='') {
        this.query_custs(1);
        return;
    }
    var url="/api/customer/search?s="+this.search+"&limit="+this.service.N_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            return;
        }
        this.fmt_customer_lines(resp.data);
        this.page.max=1;
    })
},
addCustomer() {
    var dta=copyObj(this.custInfo,['name','address','contact','cmt']);
    var reqOpts={method:"POST",url:"/api/customer/add",data:dta}
    request(reqOpts, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errDlg.showErr(resp.code, resp.info);
            return;
        }
        this.query_custs(this.page.cur);
        this.custInfo=cloneObj(EMPTY_CUST);
    })
},
shipDevice() {
    var codes=this.shipInfo.codes.split(/[(\r\n)\r\n\s\t,;]+/);
    var sellAt=new Date(this.shipInfo.sellAt).getTime()/60000;//utc分钟
    this.percent.val=0;
    if(codes.length<BATCH_NUM) {
        this.percent.each=0;//不显示
    } else {
        var n=Math.ceil(codes.length/BATCH_NUM);
        this.percent.each=1.0/n;
    }
    this.ship_batch(codes, this.shipInfo.customer, sellAt, 0);
},
showShip(i) {
    this.shipInfo={dlg:true,codes:[],
        customer:this.customers[i].id,
        name:this.customers[i].name,
        sellAt:new Date().toLocaleDateString()}
},
ship_batch(codes, customer, sellAt, start) {
    var dta={customer:customer,sellAt:sellAt,codes:[]};
    for(var n=0,i=start,l=codes.length; i<l&&n<BATCH_NUM; i++,n++) {
        dta.codes.push(codes[i]);
    }
    var opts={method:"POST",url:"/api/device/sellTo",data:dta}
    request(opts, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            this.$refs.errDlg.showErr(resp.code, resp.info);
            this.percent.val=0;
            return;
        }
        
        this.percent.val+=this.percent.each;
        if(start+BATCH_NUM < codes.length) {
            this.ship_batch(codes, customer, sellAt, start+BATCH_NUM);
            return;
        }
        this.shipInfo.dlg=false;
        this.query_custs(this.page.cur);
    });    
}
},
template:`
<q-layout view="hHh lpr fFf">
 <q-header>
  <q-toolbar>
   <q-toolbar-title>{{tags.app_name}}</q-toolbar-title>
   <q-btn flat dense icon="menu" v-if="customer.id==0">
   <q-menu>
    <q-list style="min-width:120px">
     <q-item clickable v-for="m in tags.homeMenus" @click.stop="service.jumpTo(m.url)">
      <q-item-section avatar>
      <q-icon :name="m.icon" :color="m.color"></q-icon>
      </q-item-section>
      <q-item-section>{{m.name}}</q-item-section>
     </q-item>
     <q-item clickable v-if="service.role=='admin'" @click.stop="service.jumpTo(tags.reports.url)">
      <q-item-section avatar>
       <q-icon :name="tags.reports.icon" color="red"></q-icon>
      </q-item-section>
      <q-item-section>{{tags.reports.name}}</q-item-section>
     </q-item>
    </q-list>
   </q-menu>
   </q-btn>
  </q-toolbar>
  </q-header>
  <q-footer class="bg-white q-pa-md" v-if="customer.id==0">
   <q-input outlined v-model="search" :label="tags.search" dense @keyup.enter="search_custs">
    <template v-slot:append>
     <q-icon v-show="search" name="close" @click="query_custs(1)" class="cursor-pointer"></q-icon>
     <q-icon name="search" @click="search_custs"></q-icon>
    </template>
    <template v-slot:after>
     <q-btn round color="primary" icon="add_circle" @click="custInfo.dlg=true"></q-btn>
    </template>
   </q-input>
  </q-footer>
  <q-page-container>
    <q-page class="q-pa-md">
<q-card>
 <q-card-section class="q-pa-none">
  <q-list><q-item>
   <q-item-section class="text-h6">{{customer.name}}</q-item-section>
   <q-item-section side>
    <div class="q-gutter-md text-right" style="font-size:2em">
     <q-icon name="devices" @click="service.jumpTo('/devices')" color="primary" v-if="customer.id==0"></q-icon>
     <q-icon name="list" @click="service.jumpTo('/customer?id='+customer.id)" color="primary"></q-icon>
    </div>
   </q-item-section>
  </q-item></q-list>
 </q-card-section>
 <q-card-section>
  <q-list>
   <q-item>
    <q-item-section>
     <q-item-label>{{customer.address}}</q-item-label>
     <q-item-label caption>{{customer.cmt}}</q-item-label>
    </q-item-section>
    <q-item-section side>
     <q-item-label>{{customer.createAt}}</q-item-label>
     <q-item-label caption>{{customer.contact}}</q-item-label>
     <q-item-label caption>{{tags.deviceNum}}:{{customer.deviceNum}}</q-item-label>
    </q-item-section>
   </q-item>
  </q-list>
 </q-card-section>
</q-card>
<div class="q-pa-sm flex flex-center" v-if="page.max>1">
 <q-pagination v-model="page.cur" color="primary" :max="page.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query_custs"></q-pagination>
</div>

<q-list separator>
 <q-item v-for="(c,i) in customers">
  <q-item-section>
   <q-item-label>{{c.name}}</q-item-label>
   <q-item-label caption>{{c.createAt}}</q-item-label>
  </q-item-section>
  <q-item-section>
   <q-item-label>{{c.address}}</q-item-label>
   <q-item-label caption>{{c.cmt}}</q-item-label>
   <q-item-label caption>{{c.contact}}</q-item-label>
  </q-item-section>
  <q-item-section side>
   <q-item-label>{{c.deviceNum}}</q-item-label>
   <q-item-label style="font-size:2em">
    <div class="q-gutter-md">
     <q-icon name="local_shipping" @click="showShip(i)" color="primary"></q-icon>
     <q-icon name="list" @click="service.jumpTo('/customer?id='+c.id)" color="primary"></q-icon>
    </div>
   </q-item-label>
  </q-item-section>
 </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>
<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" :close="tags.close" ref="errDlg"></component-alert-dialog>

<!-- 客户 -->
<q-dialog v-model="custInfo.dlg">
 <q-card style="min-width:75vw">
  <q-card-section>
    <div class="text-h6">{{tags.addCust}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-list>
    <q-item><q-item-section>
     <q-input v-model="custInfo.name" :label="tags.cust.name" dense maxlength=100></q-input>
    </q-item-section></q-item>
    <q-item><q-item-section>
     <q-input v-model="custInfo.address" :label="tags.cust.address" dense maxlength=85></q-input>
    </q-item-section></q-item>
    <q-item><q-item-section>
     <q-input v-model="custInfo.contact" :label="tags.cust.contact" dense maxlength=85></q-input>
    </q-item-section></q-item>
    <q-item><q-item-section>
     <q-input v-model="custInfo.cmt" :label="tags.cust.cmt" dense maxlength=300 type="textarea"></q-input>
    </q-item-section></q-item>
   </q-list>
  </q-card-section>
  <q-card-actions align="right">
    <q-btn :label="tags.ok" color="primary" @click="addCustomer"></q-btn>
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<!-- 设备发货 -->
<q-dialog v-model="shipInfo.dlg" no-backdrop-dismiss>
 <q-card style="min-width:75vw">
  <q-linear-progress :value="percent.val" color="pink" v-show="percent.val>0"></q-linear-progress>
  <q-card-section>
   <div class="text-h6">{{tags.shipDevice}}=>{{shipInfo.name}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
  <q-list>
    <q-item><q-item-section>
     <component-date-input :close="tags.ok" :label="tags.device.sellAt" v-model="shipInfo.sellAt"></component-date-input>
    </q-item-section></q-item>
    <q-item><q-item-section>
     <q-input v-model="shipInfo.codes" :label="tags.device.code"
      dense maxlength=100000 type="textarea" rows="12"></q-input>
    </q-item-section></q-item>
  </q-list>
  </q-card-section>
  <q-card-actions align="right">
    <q-btn :label="tags.ok" color="primary" @click.stop="shipDevice"></q-btn>
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>
`
}